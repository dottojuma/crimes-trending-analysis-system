import os
from rest_framework import serializers
from .models import CrimeReport

class CrimeReportSerializer(serializers.ModelSerializer):
    # Vuta majina halisi ya maandishi kutoka kwenye meza za mahusiano (ForeignKey)
    # Hii inasaidia Dashboard ya Polisi kuonyesha majina badala ya namba 1, 2, 3
    district_name = serializers.CharField(source='district.name', read_only=True)
    crime_type_name = serializers.CharField(source='crime_type.name', read_only=True)

    class Meta:
        model = CrimeReport
        # '__all__' inaruhusu fields zote ikiwemo 'status' kubadilishwa na Polisi
        fields = '__all__'

    # KAZI YA USALAMA (VALIDATION): Kukagua ukubwa na muundo wa picha ya ushahidi
    def validate_evidence_url(self, value):
        # Kama mwananchi amepandisha faili (value si tupu)
        if value and hasattr(value, 'size'):
            # MB 5 ndio kikomo cha juu cha picha ya ushahidi (5 * 1024 * 1024 bytes)
            max_size = 5 * 1024 * 1024 
            if value.size > max_size:
                raise serializers.ValidationError("Picha ni kubwa mno! Ukubwa wa picha usizidi MB 5.")
            
            # Hakikisha faili linalopakiwa linaishia na muundo wa picha pekee
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            ext = os.path.splitext(value.name)[1]
            if not ext.lower() in valid_extensions:
                raise serializers.ValidationError("Aina ya faili hailiruhusiwi. Tafadhali weka picha ya muundo wa JPG, JPEG au PNG.")
        
        return value