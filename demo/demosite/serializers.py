from demosite.models import KeyTable
from rest_framework import serializers
class KeyTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyTable
        fields = '__all__'