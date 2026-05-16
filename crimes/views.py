from rest_framework.permissions import AllowAny, IsAuthenticated  # <-- Tumeongeza AllowAny hapa
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

# 1. VIEW YA RIPOTI (Mwananchi wa kawaida kuripoti)
class CrimeReportListCreateAPIView(generics.ListCreateAPIView):
    # WANANCHI WARUHUSIWE KUTUMA RIPOTI BILA TOKEN! 🔓
    permission_classes = [AllowAny]
    
    queryset = CrimeReport.objects.all().order_by('-created_at')
    serializer_class = CrimeReportSerializer


# =======================================================
# VIEW YA UTABIRI NA ORODHA YA RIPOTI (TOKEN-SECURED)
# =======================================================
class CrimePredictionAPIView(APIView):
    # Geti limefungwa! Mtu asiye na Token hawezi kuona data hizi 🔒
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 1. TAKWIMU NA UTABIRI WA WILAYA
        district_stats = CrimeReport.objects.values('district__name').annotate(total=Count('id')).order_by('-total')
        
        predictions = []
        for stat in district_stats:
            district_name = stat['district__name']
            total_crimes = stat['total']
            
            if total_crimes > 5:
                risk_level = "HIGH (KUBWA)"
                recommendation = "Ongezeni doria maeneo haya haraka iwezekanavyo."
            else:
                risk_level = "MEDIUM (YA KATI)"
                recommendation = "Hali ipo shwari, endeleeni kufuatilia."

            predictions.append({
                "wilaya": district_name,
                "idadi_ya_matukio": total_crimes,
                "kiwango_cha_hatari_utabiri": risk_level,
                "ushauri_kwa_polisi": recommendation
            })

        # 2. ORODHA YA RIPOTI ZOTE MOJA MOJA KWA AJILI YA MEZA YA POLISI
        all_reports = CrimeReport.objects.all().order_by('-created_at')
        reports_data = []
        for r in all_reports:
            reports_data.append({
                "id": r.id,
                "description": r.description,
                "district_name": r.district.name if r.district else "Haijulikani",
                "status": r.status,
                "evidence_url": r.evidence_url.url if r.evidence_url else None,
                "latitude": r.gps_latitude,
                "longitude": r.gps_longitude,
                "tarehe": r.created_at.strftime("%Y-%m-%d %H:%M")
            })

        # 3. JAWABU LA PAMOJA KWENDA FRONTEND
        return Response({
            "status": "Success",
            "predictions": predictions,
            "reports": reports_data 
        })


class CrimeReportDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportSerializer

    # SAA ZA KAZI: Tunabadilisha ulinzi kutegemea na nani anagonga mlango
    def get_permissions(self):
        if self.request.method == 'GET':
            # Mwananchi akitaka KUSOMA tu status ya ripoti yake, ruhusu bila Token! 🔓
            return [AllowAny()]
        # Polisi akitaka KUBADILISHA (PATCH/PUT) status, lazima Token iwepo! 🔒
        return [IsAuthenticated()]

# 4. API YA POLISI KUINGIA KWENYE MFUMO (LOGIN)
@method_decorator(csrf_exempt, name='dispatch')
class PoliceLoginAPIView(APIView):
    # RUHUSU POLISI AGONGE MLANGO HUU BILA TOKEN ILI AIPATE! 🔓
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
                    "user": user.username
                })
            else:
                return Response({"status": "Failed", "message": "Akaunti hii haina mamlaka."}, status=403)
        else:
            return Response({"status": "Failed", "message": "Username au Password si sahihi!"}, status=400)


# 5. API YA POLISI KUTOKA KWENYE MFUMO (LOGOUT)
class PoliceLogoutAPIView(APIView):
    # Lazima uwe na Token ili uweze ku-logout vizuri 🔒
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Kwenye Token Auth, tunafuta token ya mtumiaji ili ashindwe kuitumia tena mpaka alog-in upya
        request.user.auth_token.delete()
        return Response({"status": "Success", "message": "Umetoka kwenye mfumo kwa mafanikio!"})