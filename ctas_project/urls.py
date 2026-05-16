from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# 1. Hakikisha umeongeza vionjo hivi viwili vipya kwenye import
from crimes.views import (
    CrimeReportListCreateAPIView, 
    CrimePredictionAPIView, 
    CrimeReportDetailAPIView,
    PoliceLoginAPIView,
    PoliceLogoutAPIView
) 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/reports/', CrimeReportListCreateAPIView.as_view(), name='crime-report-list-create'),
    # TAFUTA MSTARI HUU KWENYE crimes/urls.py NA REKEBISHA SEHEMU YA ID:
    path('api/reports/<str:pk>/', CrimeReportDetailAPIView.as_view(), name='report-detail'),
    path('api/prediction/', CrimePredictionAPIView.as_view(), name='crime-prediction'),
    
    # NJIA MPYA ZA ULINZI WA POLISI 🔒
    path('api/auth/login/', PoliceLoginAPIView.as_view(), name='police-login'),
    path('api/auth/logout/', PoliceLogoutAPIView.as_view(), name='police-logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)