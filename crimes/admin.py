from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CrimeReport, District

@admin.register(CrimeReport)
class CrimeReportAdmin(admin.ModelAdmin):
    # 1. Maeneo yatakayoonekana kwenye meza kuu ya Admin
    list_display = ('id', 'district', 'status', 'created_at', 'has_evidence', 'view_evidence_thumbnail')
    list_filter = ('status', 'district', 'created_at')
    
    # 2. SEHEMU YA UKAGUZI (Macho ya Admin):
    # Tumeongeza 'display_evidence_image' kwenye list ya kusoma tu ili Admin aone picha ndani ya ripoti
    readonly_fields = (
        'id', 'description', 'district', 'evidence_url', 
        'display_evidence_image', 'gps_latitude', 'gps_longitude', 'created_at'
    )

    # 3. PANGA MPANGILIO WA FOMU NDANI (Fields layout)
    # Hapa tunamwambia Django jinsi ya kuonyesha maelezo ndani ya ripoti
    fields = (
        'id', 'created_at', 'district', 'description', 
        'evidence_url', 'display_evidence_image', # Picha itaonekana hapa ndani ikikaguliwa
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