# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from car_classes.models import CarClass
from cars.models import Car

from utils.sales import TransactionEntityType
    

class VehicleSales(models.Model):
    CHOICES = TransactionEntityType.choices()

    created_at = models.DateTimeField(auto_now_add=True)
    car_class = models.ForeignKey(CarClass, blank=False)
    price = models.FloatField(blank=False, null=False)
    vin = models.CharField(default=None, max_length=17, blank=False, null=False)

    buyer_id = models.CharField(max_length=100, blank=False, null=False)
    buyer_type = models.CharField(max_length=25, choices=CHOICES)

    seller_id = models.CharField(max_length=100, blank=False, null=False)
    seller_type = models.CharField(max_length=25, choices=CHOICES)

    def save(self, *args, **kwargs):
        super(VehicleSales, self).save(*args, **kwargs)

    @staticmethod
    def _get_or_create_car(car_class, vin):
        car, _ = Car.objects.get_or_create(car_class=car_class, vin=vin)
        car.save()
        return car

    @staticmethod
    def _get_or_create_car_class(data):
        car_class, _ = CarClass.objects.get_or_create(**data)
        car_class.save()
        return car_class

    @classmethod
    def create_sale(cls, data):
        car_class = cls._get_or_create_car_class(data.pop('car_class'))
        car = cls._get_or_create_car(car_class, data['vin'])
        data['car_class'] = car_class
        return cls.objects.create(**data)

    @classmethod
    def update_data(cls, instance, data):
        for field in data:
            instance.__setattr__(field, data.get(field))
        instance.save()
        return instance

    class Meta:
        ordering = ('created_at',)
