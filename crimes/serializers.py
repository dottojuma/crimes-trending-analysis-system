from rest_framework import serializers
from .models import CrimeReport

class CrimeReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrimeReport
        fields = '__all__'

    # KAZI YA USALAMA (VALIDATION): Kukagua ukubwa wa picha ya ushahidi
    def validate_evidence_url(self, value):
        if value:
            # MB 5 ndio kikomo cha juu cha picha ya ushahidi (5 * 1024 * 1024 bytes)
            max_size = 5 * 1024 * 1024 
            if value.size > max_size:
                raise serializers.ValidationError("Picha ni kubwa mno! Ukubwa wa picha usizidi MB 5.")
            
            # Hakikisha faili linalopakiwa linaishia na muundo wa picha pekee
            valid_extensions = ['.jpg', '.jpeg', '.png']
            import os
            ext = os.path.splitext(value.name)[1]
            if not ext.lower() in valid_extensions:
                raise serializers.ValidationError("Aina ya faili hailiruhusiwi. Tafadhali weka picha ya muundo wa JPG au PNG.")
        
        return value