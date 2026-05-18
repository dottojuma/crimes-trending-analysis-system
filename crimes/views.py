from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status  # ONGEZA status HAPA ILI ISIGOME
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .cv_engine import analyze_image_urgency  # <--- AGIZA HAPA
# Agiza ile engine ya Machine Learning tuliyotengeneza
from .ml_engine import generate_automated_predictions
from .models import CrimeReport, District
from .serializers import CrimeReportSerializer

# =======================================================
# 1. VIEW YA RIPOTI (Mwananchi wa kawaida kuripoti)
# =======================================================
class CrimeReportListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny] # Wananchi wanaruhusiwa bila token
    queryset = CrimeReport.objects.all().order_by('-created_at')
    serializer_class = CrimeReportSerializer


# =======================================================
# 2. VIEW YA UTABIRI WA MACHINE LEARNING (TOKEN-SECURED)
# =======================================================
class CrimePredictionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # AI Spatio-Temporal Engine inapiga utabiri wa mienendo (Lini, Wapi, Kwanini)
        predictions = generate_automated_predictions()

        # Orodha ya ripoti zote moja moja kwa ajili ya meza ya Polisi
        all_reports = CrimeReport.objects.all().order_by('-created_at')
        reports_data = []
        for r in all_reports:
            
            # === COMPUTER VISION INTEGRATION ===
            # Computer Vision Engine ipigie Ramli kama kuna picha
            cv_result = {
                "cv_alert_level": "LOW 🟢",
                "cv_analytics": "Hakuna picha."
            }
            
            if r.evidence_url:
                try:
                    # Ita Computer Vision Engine
                    cv_result = analyze_image_urgency(r.evidence_url.url)
                except Exception as e:
                    cv_result = {
                        "cv_alert_level": "ERROR ⚠️",
                        "cv_analytics": f"Imeshindwa kuchambua picha: {str(e)}"
                    }

            reports_data.append({
                "id": str(r.id),
                "description": r.description,
                "district_name": r.district.name if r.district else "Haijulikani",
                "status": r.status,
                "evidence_url": r.evidence_url.url if r.evidence_url else None,
                "latitude": r.gps_latitude,
                "longitude": r.gps_longitude,
                "tarehe": r.created_at.strftime("%Y-%m-%d %H:%M"),
                
                # DATA ZA COMPUTER VISION
                "cv_alert": cv_result.get('cv_alert_level', 'LOW 🟢'),
                "cv_analytics": cv_result.get('cv_analytics', 'Hakuna uchambuzi.'),
                "cv_urgency_score": cv_result.get('cv_urgency_score', 0)
            })

        return Response({
            "status": "Success",
            "predictions": predictions,
            "reports": reports_data 
        })

# =======================================================
# 3. VIEW YA KUSHUGHULIKIA TUKIO MOJA
# =======================================================
class CrimeReportDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportSerializer

    # Kugawa ulinzi: Mwananchi asome status (GET), Askari abadilishe (PATCH)
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]


# =======================================================
# 4. API YA POLISI KUINGIA KWENYE MFUMO (LOGIN)
# =======================================================
@method_decorator(csrf_exempt, name='dispatch')
class PoliceLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({"status": "Failed", "message": "Tafadhali jaza username na password"}, status=400)
            
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff or user.is_superuser:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": "Success", 
                    "message": "Umeingia kwenye mfumo!",
                    "token": token.key,
                    "user": user.username,
                    "is_admin": bool(user.is_superuser)
                })
            else:
                return Response({"status": "Failed", "message": "Akaunti hii haina mamlaka ya ofisa."}, status=403)
        else:
            return Response({"status": "Failed", "message": "Username au Password si sahihi!"}, status=400)

# =======================================================
# 5. API YA POLISI KUTOKA KWENYE MFUMO (LOGOUT)
# =======================================================
class PoliceLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"status": "Success", "message": "Umetoka kwenye mfumo kwa mafanikio!"})

# =======================================================
# 6. API YA MWANANCHI KUFUATILIA RIPOTI KWA ID YA DATABASE
# =======================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def track_report_api(request, report_id):
    try:
        if str(report_id).isdigit():
            report = CrimeReport.objects.get(id=int(report_id))
            
            # Tafsiri ya maadili ya status kutoka herufi kubwa za database kwenda Kiswahili safi
            status_display = "Mpya / Imepokelewa"
            if report.status == 'UNDER_INVESTIGATION':
                status_display = "Inachunguzwa ⏳"
            elif report.status == 'RESOLVED' or report.status == 'RESOLVED':
                status_display = "Imeshitakiwa / Imekwisha ✅"
                
            return Response({
                "status": status_display,
                "category": report.crime_type.name if report.crime_type else "Uhalifu", # Imerekebishwa kutoka incident_type kwenda crime_type.name
                "created_at": report.created_at.strftime('%d/%m/%Y')
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Namba ya ripoti inayotafutwa lazima iwe ID ya namba tupu."}, status=status.HTTP_400_BAD_REQUEST)
        
    except CrimeReport.DoesNotExist:
        return Response({
            "error": "Namba hii ya ripoti haipatikani kwenye mfumo wako wa database."
        }, status=status.HTTP_404_NOT_FOUND)