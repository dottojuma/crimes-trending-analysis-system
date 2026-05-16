from django.contrib import admin
from django.urls import path
from crimes.views import CrimeReportListCreateAPIView

urlpatterns = [
    path('admin/', admin.site.url_urls if hasattr(admin.site, 'url_urls') else admin.site.urls),
    path('api/reports/', CrimeReportListCreateAPIView.as_view(), name='crime-report-list-create'), # Njia ya API wetu
]