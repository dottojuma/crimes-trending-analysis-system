# 🛡️ Crime Trends & Analysis System (CTAS)

**CTAS** ni mfumo wa kisasa wa kiusalama na ulinzi shirikishi ulioundwa kurahisisha utoaji wa ripoti za uhalifu kutoka kwa wananchi na kuongeza ufanisi wa Jeshi la Polisi kwa kutumia Teknolojia ya Akili Mnemba (AI & Machine Learning).

---

## 🔮 Vipengele Vikuu vya Mfumo (Key Features)

* **Lango la Mwananchi (Citizen Portal):** Wananchi wanaweza kuripoti matukio kwa haraka, kuambatisha ushahidi wa picha, na kufuatilia hatua za kiuchunguzi.
* **Computer Vision (AI) Analytics:** Mfumo unachambua picha za ushahidi papo hapo ili kugundua viwango vya dharura.
* **Machine Learning (Predictive Policing):** Unatumia algorithm ya *Random Forest* kutabiri maeneo yenye hatari, masaa ya dharura, na kutoa ushauri wa kistratejia wa doria.
* **Ulinzi na Mgawanyo wa Majukumu:** Mfumo una utambuzi wa kiotomatiki wa aina ya mtumiaji (Admin Mkuu vs Askari wa Doria) na kuwapeleka kwenye maeneo yao stahiki kiusalama.
* **Muonekano wa Kisasa:** Admin imerembwa kwa *Jazzmin Dark Theme* na kurasa za mbele zimejengwa kwa *Tailwind CSS*.

---

## 🛠️ Teknolojia Zilizotumika (Tech Stack)

**Backend:**
* Python 3.x
* Django Framework
* Django REST Framework (DRF) & Token Authentication
* Jazzmin Admin Template

**Frontend:**
* HTML5 / JavaScript (ES6 Async/Await)
* Tailwind CSS (Via CDN)

---

## 🚀 Jinsi ya Kuwasha Mradi (Installation & Setup)

### 1. Backend (Django)
Hakikisha upo kwenye folda la backend, washa mazingira yako ya mtandao (Virtual Env), kisha kimbiza seva:
```bash
# Wasisha Virtual Environment (Ubuntu)
source myenv/bin/activate

# Kimbiza seva
python manage.py runserver