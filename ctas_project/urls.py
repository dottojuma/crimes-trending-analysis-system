from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# 1. Hakikisha umeongeza CrimeReportDetailAPIView hapa kwenye import
from crimes.views import CrimeReportListCreateAPIView, CrimePredictionAPIView, CrimeReportDetailAPIView 

urlpatterns = [
    path('admin/', admin.site.url_urls if hasattr(admin.site, 'url_urls') else admin.site.urls),
    path('api/reports/', CrimeReportListCreateAPIView.as_view(), name='crime-report-list-create'),
    
    # 2. NJIA MPYA: <int:pk> inamaanisha namba ya ID ya ripoti (mfano: /api/reports/5/)
    path('api/reports/<int:pk>/', CrimeReportDetailAPIView.as_view(), name='crime-report-detail'),
    
    path('api/prediction/', CrimePredictionAPIView.as_view(), name='crime-prediction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)