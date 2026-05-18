import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ctas_project.settings') # Badilisha 'ctas_project' iwe jina la folder la settings yako
django.setup()

from crimes.models import District, PoliceStation

def piga_seed():
    print("⏳ Inaanza kuingiza vituo vya Polisi vya Dar es Salaam...")

    # Data za vituo na GPS zao kwa kila wilaya
    data_ya_vituo = {
        "Ilala": [
            {"name": "Central Police Station", "lat": -6.8161, "lon": 39.2894, "phone": "0222112233"},
            {"name": "Msimbazi Police Station", "lat": -6.8190, "lon": 39.2740, "phone": "0222114455"},
            {"name": "Buguruni Police Station", "lat": -6.8285, "lon": 39.2512, "phone": "0222116677"},
            {"name": "Stakishari Police Station", "lat": -6.8421, "lon": 39.1985, "phone": "0222118899"},
        ],
        "Kinondoni": [
            {"name": "Oysterbay Police Station", "lat": -6.7845, "lon": 39.2736, "phone": "0222151122"},
            {"name": "Magomeni Police Station", "lat": -6.8014, "lon": 39.2584, "phone": "0222153344"},
            {"name": "Mwinjuma Police Station", "lat": -6.7940, "lon": 39.2610, "phone": "0222155566"},
        ],
        "Ubungo": [
            {"name": "Ubungo Police Station", "lat": -6.8062, "lon": 39.2215, "phone": "0222181122"},
            {"name": "Mbezi Louis Police Station", "lat": -6.7925, "lon": 39.1560, "phone": "0222183344"},
            {"name": "Kijitonyama Police Station", "lat": -6.7850, "lon": 39.2440, "phone": "0222185566"},
        ],
        "Temeke": [
            {"name": "Temeke Police Station", "lat": -6.8521, "lon": 39.2745, "phone": "0222131122"},
            {"name": "Mbagala Police Station", "lat": -6.9012, "lon": 39.2715, "phone": "0222133344"},
            {"name": "Chang'ombe Police Station", "lat": -6.8420, "lon": 39.2690, "phone": "0222135566"},
        ],
        "Kigamboni": [
            {"name": "Kigamboni Police Station", "lat": -6.8250, "lon": 39.3190, "phone": "0222171122"},
            {"name": "Mjimwema Police Station", "lat": -6.8480, "lon": 39.3520, "phone": "0222173344"},
        ]
    }

    for wilaya_name, vituo in data_ya_vituo.items():
        # Tafuta au tengeneza wilaya kwanza
        wilaya, _ = District.objects.get_or_create(name=wilaya_name)
        
        for k in vituo:
            station, created = PoliceStation.objects.get_or_create(
                name=k["name"],
                district=wilaya,
                defaults={
                    "latitude": k["lat"],
                    "longitude": k["lon"],
                    "phone_number": k["phone"]
                }
            )
            if created:
                print(f"✅ Kituo kimeingizwa: {k['name']} ({wilaya_name})")
            else:
                print(f"ℹ️ Kituo tayari kipo: {k['name']}")

    print("🚀 Vituo vyote vimepakiwa kikamilifu database!")

if __name__ == '__main__':
    piga_seed()