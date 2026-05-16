from django.contrib import admin
from .models import District, CrimeType, CrimeReport

# Kusajili meza zetu ili zionekane Admin
admin.site.register(District)
admin.site.register(CrimeType)
admin.site.register(CrimeReport)