from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CrimeReport, District, PoliceStation

@admin.register(CrimeReport)
class CrimeReportAdmin(admin.ModelAdmin):
    # 1. Maeneo yatakayoonekana kwenye meza kuu ya Admin
    # Tumeongeza 'police_station' ili kuona kituo kilichopangiwa kwenye meza kuu
    list_display = ('id', 'district', 'police_station', 'status', 'created_at', 'has_evidence', 'view_evidence_thumbnail')
    list_filter = ('status', 'district', 'police_station', 'created_at')
    
    # 2. SEHEMU YA UKAGUZI (Macho ya Admin):
    readonly_fields = (
        'id', 'description', 'district', 'evidence_url', 
        'display_evidence_image', 'gps_latitude', 'gps_longitude', 'created_at'
    )

    # 3. PANGA MPANGILIO WA FOMU NDANI (Fields layout)
    # Tumeongeza 'police_station' hapa ili Admin aweze kuchagua au kubadili kituo doria
    fields = (
        'id', 'created_at', 'district', 'police_station', 'description', 
        'evidence_url', 'display_evidence_image', 
        'gps_latitude', 'gps_longitude', 'status'
    )

    # FUNCTION A: Inachora picha ndogo (Thumbnail) kwenye meza kuu ya nje
    def view_evidence_thumbnail(self, obj):
        if obj.evidence_url:
            return mark_safe(f'<img src="{obj.evidence_url.url}" style="width: 50px; height: auto; border-radius: 4px; border: 1px solid #444;" />')
        return "Hakuna Picha"
    view_evidence_thumbnail.short_description = "Ushahidi (Nje)"

    # FUNCTION B: Inafungua picha kubwa ya kukaguliwa (Preview) ndani ya ripoti
    def display_evidence_image(self, obj):
        if obj.evidence_url:
            return mark_safe(f'''
                <div style="margin-top: 10px;">
                    <a href="{obj.evidence_url.url}" target="_blank">
                        <img src="{obj.evidence_url.url}" style="max-width: 400px; height: auto; border-radius: 8px; border: 2px solid #6366f1; box-shadow: 0 4px 6px rgba(0,0,0,0.3);" />
                    </a>
                    <p style="color: #888; font-size: 11px; mt-1;">💡 Bofya kwenye picha kuifungua kwa ukubwa kamili (Tab Mpya).</p>
                </div>
            ''')
        return "Mwananchi hakupandisha ushahidi wa picha."
    display_evidence_image.short_description = "Ukaguzi wa AI & Picha ya Ushahidi"

    def has_evidence(self, obj):
        return bool(obj.evidence_url)
    has_evidence.boolean = True
    has_evidence.short_description = "Ina Ushahidi?"


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# ==========================================
# USAJILI MPYA: KITUO VYA POLISI (USING DECORATOR)
# ==========================================
@admin.register(PoliceStation)
class PoliceStationAdmin(admin.ModelAdmin):
    # Inatengeneza meza safi ya kuorodhesha vituo, coordinates zao na namba za simu
    list_display = ('id', 'name', 'district', 'latitude', 'longitude', 'phone_number')
    list_filter = ('district',)
    search_fields = ('name', 'phone_number')