from __future__ import unicode_literals

from django.db import models
from utils.sales import TransactionEntityType
 	
 	
class Individual(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    license_no = models.CharField(max_length=25, blank=False, null=False)
    ssn_last_4 = models.IntegerField(blank=False, null=False)
    dob = models.CharField(max_length=25, blank=False, null=False)

    def type(self):
    	return TransactionEntityType.individual.value

    class Meta:
        ordering = ('created_at',)
