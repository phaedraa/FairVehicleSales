from __future__ import unicode_literals

from django.db import models
from car_classes.models import CarClass
 	
class Car(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    vin = models.CharField(max_length=17, unique=True, blank=False, null=False)
    car_class = models.ForeignKey(CarClass, blank=False, null=False)


    class Meta:
        ordering = ('created_at',)
