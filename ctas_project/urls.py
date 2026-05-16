from django.contrib import admin
from django.urls import path
from django.conf import settings # <-- Tumeongeza hii
from django.conf.urls.static import static # <-- Tumeongeza hii
from crimes.views import CrimeReportListCreateAPIView, CrimePredictionAPIView

urlpatterns = [
    path('admin/', admin.site.url_urls if hasattr(admin.site, 'url_urls') else admin.site.urls),
    path('api/reports/', CrimeReportListCreateAPIView.as_view(), name='crime-report-list-create'),
    path('api/prediction/', CrimePredictionAPIView.as_view(), name='crime-prediction'),
]

# Hii mistari inaiambia Django kuruhusu picha zilizopo kwenye folda la media zionekane mtandaoni wakati wa majaribio
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)