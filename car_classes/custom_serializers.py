from rest_framework import serializers, viewsets, routers
from .models import CarClass

class CarClassSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
    	for field in validated_data:
            instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance


    class Meta:
        model = CarClass
        fields = ('model', 'make', 'year')

