# Crimes Trending Analysis System (CTAS)

## 📌 Project Overview
Huu ni mfumo wa kidijitali wa ufuatiliaji na utabiri wa mwenendo wa uhalifu katika Mkoa wa Dar es Salaam (Wilaya za Temeke, Kigamboni, Ubungo, Ilala, na Kinondoni). Mfumo huu unawawezesha wananchi kuripoti matukio, na unajumuisha mfumo wa uchambuzi wa takwimu unaosaidia Jeshi la Polisi kutabiri maeneo yenye hatari kubwa ya uhalifu (**Crime Hotspots**).

## 🚀 Key Features (Sifa Kuu)
1. **Multi-Media Crime Reporting:** Wananchi wanaweza kuripoti matukio kwa maandishi na maelezo kamili.
2. **REST API Architecture:** Mfumo una API imara inayoruhusu mifumo ya nje (App za simu/Web) kutuma na kusoma ripoti.
3. **Predictive Analytics Engine:** Mfumo unasoma data zilizopo na kupiga hesabu kiotomatiki kubaini viwango vya hatari kwa kila wilaya na kutoa ushauri wa kiutendaji kwa polisi.
4. **Django Admin Dashboard:** Jopo la uongozi lililojumuishwa kwa ajili ya usimamizi wa data na sasisho za matukio.

## 🛠️ Tech Stack (Zana Zilizotumika)
* **Backend Framework:** Python (Django 5.x)
* **API Development:** Django REST Framework (DRF)
* **Database:** SQLite (Inaweza kuhamishiwa PostgreSQL kwa urahisi)

## 🔌 API Endpoints (Njia za API)
* `GET /api/reports/` - Kusoma ripoti zote za uhalifu zilizotumwa.
* `POST /api/reports/` - Kuripoti tukio jipya kutoka kwenye App au Web.
* `GET /api/prediction/` - Ukurasa maalum wa Polisi unaoonyesha uchambuzi na utabiri wa usalama wa wilaya zote.

## 💻 Jinsi ya Kuwasha Mradi Huu (Setup Instructions)

Kama unataka kuwasha mradi huu kwenye kompyuta yako, fuata hatua hizi:

1. **Clone mradi kutoka GitHub:**
   ```bash
   git clone [https://github.com/dottojuma/crimes-trending-analysis-system.git](https://github.com/dottojuma/crimes-trending-analysis-system.git)
   cd crimes-trending-analysis-system