import json
from django.forms.models import model_to_dict
from rest_framework import serializers, viewsets, routers
from .models import VehicleSales
from cars.models import Car
from car_classes.models import CarClass
from car_classes.serializers import CarClassSerializer


class VehicleSalesSerializer:

    def __init__(self, instance=None, data=None):
        self.fields = ('buyer_id', 'buyer_type', 'seller_id',
            'seller_type', 'price', 'vin', 'car_class', 'created_at')
        self.is_valid_called = False
        self._data = {}
        self._instance = None
        if instance and data:
            self._instance = self.update(instance, data)
        elif data:
            self._instance = self.create(data)
            print('instance', self._instance)
        elif instance:
            self.instance = instance
            self.is_valid()


    def instance(self):
        return self._instance


    def is_valid(self):
        self.is_valid_called = True
        return isinstance(self._instance, VehicleSales)


    def save(self):
        if not self.is_valid_called:
            raise Exception("Required call to is_valid first")


    def data(self):
        if not self.is_valid_called:
            raise Exception("Required call to is_valid first")

        if not self._instance:
            return {}

        dict_m = model_to_dict(self._instance)
        dict_m['car_class'] = model_to_dict(self._instance.car_class)
        dict_m['created_at'] = self._instance.created_at
        self._data = dict_m
        return self._data


    def get_or_create_car(self, car_class, vin):
        car, _ = Car.objects.get_or_create(car_class=car_class, vin=vin)
        car.save()
        self.car = car
        return car


    def get_or_create_car_class(self, data):
        car_class, _ = CarClass.objects.get_or_create(**data)
        car_class.save()
        self.car_class = car_class
        return car_class


    def create(self, validated_data):
        print('IN CREATE')
        car_class = self.get_or_create_car_class(validated_data.pop('car_class'))
        print('car_class', car_class.id)
        car = self.get_or_create_car(car_class, validated_data.get('vin'))
        print('car', car.id)
        sale = VehicleSales(
            seller_id=validated_data.get('seller_id'),
            seller_type=validated_data.get('seller_type'),
            buyer_id=validated_data.get('buyer_id'),
            buyer_type=validated_data.get('buyer_type'),
            car_class=car_class,
            vin=validated_data.get('vin'),
            price=validated_data.get('price'),
        )
        sale.save()
        print('sale!', sale)
        return sale


    def update(self, instance, validated_data):
        print("update")
    	for field in validated_data:
            instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance


##

import serpy
from .models import VehicleSales
from car_classes.serializers import CarClassSerializer


class VehicleSalesSerializer(serpy.Serializer):
    seller_id = serpy.IntField()
    seller_type = serpy.Field()
    buyer_id = serpy.IntField()
    buyer_type = serpy.Field()
    car_class = serpy.Field()
    vin = serpy.Field()
    price = serpy.FloatField()
    created_at = serpy.Field()
    id = serpy.IntField()
    car_class = serpy.MethodField()


    def get_car_class(self, obj):
        serialized = CarClassSerializer(obj.car_class)
        return serialized.data
##



class VehicleSalesSerializer(serializers.ModelSerializer):
    car_class = CarClassSerializer()


    def get_or_create_car(self, car_class, vin):
        car, _ = Car.objects.get_or_create(car_class=car_class, vin=vin)
        car.save()
        return car


    def get_or_create_car_class(self, data):
        car_class, _ = CarClass.objects.get_or_create(**data)
        car_class.save()
        return car_class


    def create(self, validated_data):
        print('IN CREATE')
        car_class = self.get_or_create_car_class(validated_data.pop('car_class'))
        print('car_class', car_class.id)
        car = self.get_or_create_car(car_class, validated_data.get('vin'))
        print('car', car.id)
        sale = VehicleSales(
            seller_id=validated_data.get('seller_id'),
            seller_type=validated_data.get('seller_type'),
            buyer_id=validated_data.get('buyer_id'),
            buyer_type=validated_data.get('buyer_type'),
            car_class=car_class,
            vin=validated_data.get('vin'),
            price=validated_data.get('price'),
        )
        sale.save()
        return sale


    def update(self, instance, validated_data):
        print("update")
        for field in validated_data:
            instance.__setattr__(field, validated_data.get(field))
        instance.save()
        return instance


    class Meta:
        model = VehicleSales
        fields = ('buyer_id', 'buyer_type', 'seller_id',
            'seller_type', 'price', 'vin')