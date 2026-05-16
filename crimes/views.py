from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from .models import CrimeReport, District
from .serializers import CrimeReportSerializer

# 1. VIEW YA KAWAIDA YA RIPOTI (Hii ilikuwepo)
class CrimeReportListCreateAPIView(generics.ListCreateAPIView):
    queryset = CrimeReport.objects.all().order_by('-created_at')
    serializer_class = CrimeReportSerializer

# 2. VIEW MPYA YA UTABIRI (Hakikisha herufi zinalingana kabisa na za urls.py)
class CrimePredictionAPIView(APIView):
    def get(self, request):
        # 1. Takwimu za Wilaya (kama mwanzo)
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

        # 2. SEHEMU MPYA: Leta orodha ya ripoti zote moja moja kwa ajili ya Dashboard ya Polisi
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

        return Response({
            "status": "Success",
            "predictions": predictions,
            "reports": reports_data # Tunasafirisha na ripoti zote moja moja hapa
        })
    # KAZI MPYA: Inaruhusu kusoma tukio moja maalum au kulisadisha (Update)
class CrimeReportDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = CrimeReport.objects.all()
    serializer_class = CrimeReportSerializer