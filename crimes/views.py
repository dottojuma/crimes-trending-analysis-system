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
        # Kupata idadi ya ripoti kwa kila wilaya
        district_stats = CrimeReport.objects.values('district__name').annotate(total=Count('id')).order_by('-total')
        
        predictions = []
        for stat in district_stats:
            district_name = stat['district__name']
            total_crimes = stat['total']
            
            # Algorithm ya utabiri na viwango vya hatari
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

        return Response({
            "status": "Success",
            "message": "Utabiri wa mwenendo wa uhalifu Dar es Salaam",
            "data": predictions
        })