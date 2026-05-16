from django.contrib import admin
from django.urls import path
# 1. Tumeagiza (import) CrimePredictionAPIView kutoka kwenye views zetu
from crimes.views import CrimeReportListCreateAPIView, CrimePredictionAPIView 

urlpatterns = [
    path('admin/', admin.site.url_urls if hasattr(admin.site, 'url_urls') else admin.site.urls),
    
    # Njia ya mwananchi kutuma na kusoma ripoti
    path('api/reports/', CrimeReportListCreateAPIView.as_view(), name='crime-report-list-create'), 
    
    # 2. NJIA MPYA: Njia ya polisi kuona utabiri na uchambuzi wa wilaya zote
    path('api/prediction/', CrimePredictionAPIView.as_view(), name='crime-prediction'), 
]