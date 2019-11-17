from demosite.models import KeyTable, ApartmentFeature
from rest_framework import serializers

class KeyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyTable
        fields = '__all__'

#class ApartmentFeatureSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ApartmentFeature
#        fields = '__all__'
