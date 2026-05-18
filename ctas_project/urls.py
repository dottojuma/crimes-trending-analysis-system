from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from crimes import views  # Hii inatosha kuvuta views zote za crimes app

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. Hii ndio njia yako halisi ya kiasili ya KUTUMA na KUSOMA ripoti zote kwenye DB
    path('api/reports/', views.CrimeReportListCreateAPIView.as_view(), name='crime-report-list-create'),
    
    # 2. Hii ni kwa ajili ya kuona ripoti moja kwa ID yake ya database
    path('api/reports/detail/<str:pk>/', views.CrimeReportDetailAPIView.as_view(), name='report-detail'),
    
    # 3. NJIA YA MWANANCHI KUFUATILIA RIPOTI KWA REFERENCE NUMBER
    path('api/reports/track/<str:report_id>/', views.track_report_api, name='track-report-api'),
    
    # 4. NJIA MPYA YA VITUO VYA POLISI (IMEREKEBISHWA KUTOKEA KWA VIEWS ZA CRIMES)
    path('api/stations/', views.PoliceStationListAPIView.as_view(), name='police-station-list'),
    
    # 5. AI & prediction
    path('api/prediction/', views.CrimePredictionAPIView.as_view(), name='crime-prediction'),
    
    # NJIA ZA AUTHENTICATION ZA POLISI 🔒
    path('api/auth/login/', views.PoliceLoginAPIView.as_view(), name='police-login'),
    path('api/auth/logout/', views.PoliceLogoutAPIView.as_view(), name='police-logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)