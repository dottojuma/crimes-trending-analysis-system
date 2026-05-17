from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import CrimeReport, District
from .serializers import CrimeReportSerializer
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token 
from .cv_engine import analyze_image_urgency # <--- AGIZA HAPA
# Agiza ile engine ya Machine Learning tuliyotengeneza
from .ml_engine import generate_automated_predictions

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
            # Kama ripoti ina picha, tuiandishe kwa CV Engine ipigie Ramli
            cv_result = {
                "cv_alert_level": "LOW 🟢",
                "cv_analytics": "Hakuna picha."
            }
            
            if r.evidence_url:
                # Ita Computer Vision Engine
                # cv_result itapata data: {'cv_alert_level': '...', 'cv_analytics': '...'}
                cv_result = analyze_image_urgency(r.evidence_url.url)

            reports_data.append({
                "id": str(r.id),
                "description": r.description,
                "district_name": r.district.name if r.district else "Haijulikani",
                "status": r.status,
                "evidence_url": r.evidence_url.url if r.evidence_url else None,
                "latitude": r.gps_latitude,
                "longitude": r.gps_longitude,
                "tarehe": r.created_at.strftime("%Y-%m-%d %H:%M"),
                
                # ONGEZA DATA ZA COMPUTER VISION HAPA
                "cv_alert": cv_result['cv_alert_level'],
                "cv_analytics": cv_result['cv_analytics'],
                "cv_urgency_score": cv_result.get('cv_urgency_score', 0)
            })

        return Response({
            "status": "Success",
            "predictions": predictions,
            "reports": reports_data 
        })
# =======================================================
# 3. VIEW YA KUSHUGHULIKIA TUKIO MOJA (Hapa ndipo palikuwa na Error!)
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
        
        # Hapa sasa nafasi zimekaa sawa kiuhakika ndani ya def post:
        if user is not None:
            if user.is_staff or user.is_superuser:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": "Success", 
                    "message": "Umeingia kwenye mfumo!",
                    "token": token.key,
                    "user": user.username,
                    "is_admin": bool(user.is_superuser)  # Inarudisha true/false safi
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
            # Futa token ya huyu askari kwenye database kwa usalama
            request.user.auth_token.delete()
        except:
            pass
        logout(request)
        return Response({"status": "Success", "message": "Umetoka kwenye mfumo kwa mafanikio!"})