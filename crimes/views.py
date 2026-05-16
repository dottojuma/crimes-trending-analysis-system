from rest_framework import generics
from .models import CrimeReport
from .serializers import CrimeReportSerializer

# View ya kuonyesha ripoti zote na kuruhusu watu kutuma ripoti mpya
class CrimeReportListCreateAPIView(generics.ListCreateAPIView):
    queryset = CrimeReport.objects.all().order_by('-created_at')
    serializer_class = CrimeReportSerializer