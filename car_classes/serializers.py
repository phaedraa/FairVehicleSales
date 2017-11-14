import serpy
from rest_framework import serializers, viewsets, routers
from .models import CarClass

class CarClassSerializer(serpy.Serializer):
    
    make = serpy.Field()
    model = serpy.Field()
    year = serpy.IntField()
