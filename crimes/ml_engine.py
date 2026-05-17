import pandas as pd
import datetime
from django.db.models import Count
from django.db.models.functions import ExtractMonth, ExtractDay, ExtractHour
from .models import CrimeReport, District
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def generate_automated_predictions():
    # 1. Vuta data zenye vionjo vya muda (Saa, Siku, Mwezi)
    reports = CrimeReport.objects.all().annotate(
        mwezi=ExtractMonth('created_at'),
        siku=ExtractDay('created_at'),
        saa=ExtractHour('created_at')
    ).values('district_id', 'district__name', 'mwezi', 'siku', 'saa', 'status', 'description')

    if not reports.exists():
        return []

    df = pd.DataFrame(list(reports))

    # Feature Engineering ya maandalizi ya AI
    district_counts = df.groupby('district_id').size().to_dict()
    df['total_district_crimes'] = df['district_id'].map(district_counts)

    # Maandalizi ya X (Vigezo) na y (Utabiri wa Hatari: 0=Salama, 1=Tahadhari, 2=Kashfa/Hatari)
    X = df[['mwezi', 'siku', 'saa', 'total_district_crimes']]
    y = np.where(df['total_district_crimes'] > 5, 2, np.where(df['total_district_crimes'] > 2, 1, 0))

    # Kufundisha Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    all_districts = District.objects.all()
    automated_results = []
    sasa = datetime.datetime.now()

    for district in all_districts:
        df_district = df[df['district_id'] == district.id]
        current_count = district_counts.get(district.id, 0)

        # 🕒 A) KUCHUNGUZA "LINI" (Saa za Hatari zilizojificha)
        # AI inachambua ni masaa gani yamebeba matukio mengi kwenye wilaya hii
        if not df_district.empty:
            saa_zinazoongoza = df_district.groupby('saa').size().sort_values(ascending=False)
            saa_ya_hatari_zaidi = int(saa_zinazoongoza.index[0])
            muda_wa_hatari = f"{saa_ya_hatari_zaidi}:00 hadi {saa_ya_hatari_zaidi + 2}:00"
        else:
            muda_wa_hatari = "Saa za usiku wa manane (00:00 - 04:00)"

        # 🧠 B) KUCHUNGUZA "KWA NINI" (Uchambuzi wa Sababu na Mienendo - Analytics)
        # AI inasoma maneno muhimu kwenye description kubaini sababu kubwa
        sababu_kuu = "Mkusanyiko wa dharura na uhalifu wa hapa na pale."
        if not df_district.empty:
            maneno_mapezi = " ".join(df_district['description'].astype(str)).lower()
            if "wizi" in maneno_mapezi or "kuibiwa" in maneno_mapezi:
                sababu_kuu = "Mwenendo unaonyesha ongezeko la vikundi vya uporaji na uvunjaji wa nyumba."
            elif "vurugu" in maneno_mapezi or "kupigana" in maneno_mapezi:
                sababu_kuu = "Kuna ishara ya migogoro ya kijamii au maeneo ya starehe yasiyo na ulinzi."
            elif "silaha" in maneno_mapezi or "panga" in maneno_mapezi:
                sababu_kuu = "Tahadhari! Kuna mienendo ya uhalifu wa kutumia nguvu na silaha za jadi."

        # C) UTABIRI WA BAADAE
        future_scenario = pd.DataFrame([{
            'mwezi': sasa.month,
            'siku': sasa.day,
            'saa': sasa.hour,
            'total_district_crimes': current_count
        }])
        
        prediction_code = model.predict(future_scenario)[0]
        confidence = round(np.max(model.predict_proba(future_scenario)) * 100, 1)

        if prediction_code == 2:
            risk_level = "CRITICAL RISK 🔴"
            color_tag = "text-red-400 border-red-500/30 bg-red-500/10"
        elif prediction_code == 1:
            risk_level = "WARNING RISK 🟡"
            color_tag = "text-yellow-400 border-yellow-500/30 bg-yellow-500/10"
        else:
            risk_level = "STABLE 🟢"
            color_tag = "text-emerald-400 border-emerald-500/30 bg-emerald-500/10"

        automated_results.append({
            "wapi": district.name,
            "idadi_ya_matukio": current_count,
            "kiwango_cha_hatari": risk_level,
            "color_tag": color_tag,
            "lini_saa_za_hatari": muda_wa_hatari,
            "kwa_nini_sababu": sababu_kuu,
            "ai_confidence": f"{confidence}%"
        })

    return automated_results