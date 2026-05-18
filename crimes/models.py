from django.db import models

# 1. Meza ya Wilaya (Districts)
class District(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# 2. Meza ya Aina za Uhalifu (Crime Types)
class CrimeType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
# 1. MODEL MPYA YA VITUO VYA POLISI
class PoliceStation(models.Model):
    name = models.CharField(max_length=100, verbose_name="Jina la Kituo")
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='stations', verbose_name="Wilaya")
    latitude = models.FloatField(verbose_name="GPS Latitude")
    longitude = models.FloatField(verbose_name="GPS Longitude")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Namba ya Simu ya Kituo")

    class Meta:
        verbose_name_plural = "Vituo vya Polisi"

    def __str__(self):
        return f"{self.name} ({self.district.name})"

# 3. Meza Kuu ya Taarifa za Matukio (Crime Reports)
class CrimeReport(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Mpya / Imepokelewa'),
        ('UNDER_INVESTIGATION', 'Inachunguzwa'),
        ('RESOLVED', 'Imeshitakiwa / Imekwisha'),
    ]

    district = models.ForeignKey(District, on_delete=models.CASCADE)
    crime_type = models.ForeignKey(CrimeType, on_delete=models.CASCADE)
    description = models.TextField()
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    
    # ONGEZA FIELD HII HAPA CHINI:
    police_station = models.ForeignKey(
        PoliceStation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reports',
        verbose_name="Kituo Kilichopangiwa Tukio"
    )
    # Tumeibadilisha kutoka URLField kwenda ImageField. 
    # upload_to='crimes_evidence/' ina maana picha zitaingia ndani ya media/crimes_evidence/
    # blank=True, null=True ina maana mwananchi anaweza kuripoti hata bila kuweka picha (hiari)
    evidence_url = models.ImageField(upload_to='crimes_evidence/', blank=True, null=True)
    gps_latitude = models.FloatField()
    gps_longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True) # Muda na tarehe kiotomatiki
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='NEW')

    def __str__(self):
        return f"{self.crime_type.name} - {self.district.name} ({self.created_at.strftime('%Y-%m-%d')})"