from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status  
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import math

from .cv_engine import analyze_image_urgency  
from .ml_engine import generate_automated_predictions
from .models import CrimeReport, District, PoliceStation  # ONGEZA PoliceStation hapa
from .serializers import CrimeReportSerializer

# =======================================================
# 0. FOMULA YA KIJIOGRAFIA (HAVERSINE FORMULA)
# =======================================================
def tafuta_umbali_wa_gps(lat1, lon1, lat2, lon2):
    """
    Inapiga hesabu ya umbali wa kilomita (km) kati ya pointi mbili za GPS duniani.
    """
    R = 6371.0  # Kipenyo cha dunia kwa kilomita
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


# =======================================================
# 1. VIEW YA RIPOTI (Mwananchi wa kawaida kuripoti - IMPROVED)
# =======================================================
class CrimeReportListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny] # Wananchi wanaruhusiwa bila token
    queryset = CrimeReport.objects.all().order_by('-created_at')
    serializer_class = CrimeReportSerializer

    def perform_create(self, serializer):
        # Tunahifadhi ripoti ya kwanza ili kupata object yake
        report = serializer.save()
        
        # AUTOMATED GPS MATCHING LOGIC
        mwananchi_lat = self.request.data.get('gps_latitude')
        mwananchi_lon = self.request.data.get('gps_longitude')
        
        if mwananchi_lat and mwananchi_lon:
            try:
                lat1 = float(mwananchi_lat)
                lon1 = float(mwananchi_lon)
                
                vituo_vyote = PoliceStation.objects.all()
                kituo_cha_karibu = None
                umbali_mdogo_zaidi = float('inf')
                
                # Mtambo unazunguka kutafuta kituo cha karibu Dar es Salaam
                for kituo in vituo_vyote:
                    umbali = tafuta_umbali_wa_gps(lat1, lon1, kituo.latitude, kituo.longitude)
                    if umbali < umbali_mdogo_zaidi:
                        umbali_mdogo_zaidi = umbali
                        kituo_cha_karibu = kituo
                
                if kituo_cha_karibu:
                    report.police_station = kituo_cha_karibu
                    report.save()
                    print(f"🚨 AI GEOSPATIAL: Tukio #{report.id} limeunganishwa na {kituo_cha_karibu.name} (Umbali: {umbali_mdogo_zaidi:.2f} Km)")
            except Exception as e:
                print(f"Kosa la kiufundi kwenye kupiga hesabu ya GPS: {e}")
                
        # MANUAL FALLBACK: Kama GPS haikuwepo ila kadi ilichagua Kituo kwa Dropdown
        elif self.request.data.get('police_station'):
            try:
                station_id = self.request.data.get('police_station')
                report.police_station = PoliceStation.objects.get(id=int(station_id))
                report.save()
            except (PoliceStation.DoesNotExist, ValueError):
                pass


# =======================================================
# 1B. API ENDPOINT MPYA: KUVUTA ORODHA YA VITUO (Kwa dropdown au ramani)
# =======================================================
class PoliceStationListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        district_id = request.query_params.get('district_id')
        if district_id:
            vituo = PoliceStation.objects.filter(district_id=district_id)
        else:
            vituo = PoliceStation.objects.all()
            
        data_ya_vituo = []
        for v in vituo:
            data_ya_vituo.append({
                "id": v.id,
                "name": v.name,
                "district_id": v.district.id if v.district else None,
                "district_name": v.district.name if v.district else "Haijulikani",
                "latitude": v.latitude,
                "longitude": v.longitude,
                "phone_number": v.phone_number if v.phone_number else "N/A"
            })
        return Response({"status": "Success", "stations": data_ya_vituo}, status=status.HTTP_200_OK)


# =======================================================
# 2. VIEW YA UTABIRI WA MACHINE LEARNING (TOKEN-SECURED)
# =======================================================
class CrimePredictionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        predictions = generate_automated_predictions()
        all_reports = CrimeReport.objects.all().order_by('-created_at')
        reports_data = []
        
        for r in all_reports:
            cv_result = {
                "cv_alert_level": "LOW 🟢",
                "cv_analytics": "Hakuna picha."
            }
            
            if r.evidence_url:
                try:
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
                "police_station_name": r.police_station.name if r.police_station else "Hakijaamuliwa 👮‍♂️", # MAPYA YA VITUO
                "status": r.status,
                "evidence_url": r.evidence_url.url if r.evidence_url else None,
                "latitude": r.gps_latitude,
                "longitude": r.gps_longitude,
                "tarehe": r.created_at.strftime("%Y-%m-%d %H:%M"),
                
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
            
            status_display = "Mpya / Imepokelewa"
            if report.status == 'UNDER_INVESTIGATION':
                status_display = "Inachunguzwa ⏳"
            elif report.status == 'RESOLVED':
                status_display = "Imeshitakiwa / Imekwisha ✅"
                
            return Response({
                "status": status_display,
                "category": report.crime_type.name if report.crime_type else "Uhalifu", 
                "created_at": report.created_at.strftime('%d/%m/%Y')
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Namba ya ripoti inayotafutwa lazima iwe ID ya namba tupu."}, status=status.HTTP_400_BAD_REQUEST)
        
    except CrimeReport.DoesNotExist:
        return Response({
            "error": "Namba hii ya ripoti haipatikani kwenye mfumo wako wa database."
        }, status=status.HTTP_404_NOT_FOUND)