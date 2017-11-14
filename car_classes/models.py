from __future__ import unicode_literals

from django.db import models

 	
class CarClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    model = models.CharField(max_length=100, blank=False, null=False)
    make = models.CharField(max_length=100, blank=False, null=False)
    year = models.IntegerField(blank=False, null=False)


    class Meta:
        ordering = ('created_at',)
