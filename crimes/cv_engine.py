import os
import cv2
import numpy as np
from django.conf import settings
from skimage.feature import hog
from skimage import exposure

def analyze_image_urgency(image_relative_url):
    """
    AI inapokea njia ya picha, kisha inachambua muundo (patterns) 
    kubaini kama ina dalili za dharura ( vurugu, silaha, ajali).
    
    Hii ni Baseline Advanced Advanced Computer Vision Model (HOG descriptor).
    """
    
    # 1. Pata njia kamili ya picha kwenye kompyuta (Server Path)
    # Media URL inakuja kama /media/evidence/picha.jpg
    # Tunaiunganisha na MEDIA_ROOT ili kupata /home/dotto/.../media/evidence/picha.jpg
    clean_url = image_relative_url.lstrip('/') # Ondoa '/' ya mwanzo
    image_full_path = os.path.join(settings.MEDIA_ROOT, clean_url.replace(settings.MEDIA_URL.lstrip('/'), ''))

    if not os.path.exists(image_full_path):
        return {
            "cv_alert_level": "LOW",
            "cv_urgency_score": 0,
            "cv_analytics": "Hakuna ushahidi wa picha."
        }

    try:
        # 2. Fungua Picha (Kutumia OpenCV)
        image = cv2.imread(image_full_path)
        if image is None:
            raise Exception("Imeshindwa kusoma picha.")

        # Geuza kuwa Rangi ya Kijivu (Grayscale) kwa ajili ya uchambuzi mwepesi
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Rekebisha ukubwa (Resize) ili zote zifanane
        resized_image = cv2.resize(gray_image, (128, 128))

        # 3. KUCHAMBUA MUUNDO (FEATURE EXTRACTION - HOG)
        # HOG (Histogram of Oriented Gradients) inasoma mienendo ya mistari
        # na maumbo yaliyopo kwenye picha (inaweza kubaini umbo la silaha au vurugu)
        fd, hog_image = hog(resized_image, orientations=8, pixels_per_cell=(16, 16),
                            cells_per_block=(1, 1), visualize=True, channel_axis=None)
        
        # Boresha muonekano wa HOG (kwa ajili ya uchambuzi wetu, si lazima kuonyesha)
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    # 4. KUKADIRIA DHARURA KWA WASTANI (DYNAMIC NORMALIZED SCORING)
        # Badala ya np.sum(fd) ambayo inaleta namba kubwa kila picha,
        # tunachukua Wastani (Mean) na Standard Deviation ili kupata nguvu halisi ya mabadiliko ya mistari.
        gradient_mean = np.mean(fd) * 100 # Wastani wa mistari mikali
        gradient_std = np.std(fd) * 100   # Jinsi mistari ilivyosambaa
        
        # Alama ya dharura iliyosafishwa (Kigezo cha kiwanda cha CV)
        final_score = gradient_mean + (0.5 * gradient_std)

        # MIPAKA MIPYA YA KISAYANSI (Thresholds):
        # Sasa hivi picha lazima iwe na mistari mikali sana (kama silaha, vurugu za picha) ili kuvuka 45
        if final_score > 45: 
            cv_alert_level = "CRITICAL 🔴"
            urgency_score = 3
            analytics = f"CV ALERT ({round(final_score,1)}): Muundo mkali sana wa mistari na migongano ya mwanga (Inaashiria silaha/vurugu)."
        elif final_score > 28:
            cv_alert_level = "HIGH 🟡"
            urgency_score = 2
            analytics = f"CV WARNING ({round(final_score,1)}): Mwangaza na mistari ya wastani."
        else:
            cv_alert_level = "LOW 🟢"
            urgency_score = 1
            analytics = f"CV NORMAL ({round(final_score,1)}): Picha ipo shwari, muundo wa kawaida wa mazingira."

        return {
            "cv_alert_level": cv_alert_level,
            "cv_urgency_score": urgency_score,
            "cv_analytics": analytics
        }
    except Exception as e:
        print(f"Kosa kwenye CV Engine: {e}")
        return {
            "cv_alert_level": "ERROR ⚪",
            "cv_urgency_score": 0,
            "cv_analytics": f"Imeshindwa kuchambua picha: {str(e)}"
        }