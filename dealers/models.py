from __future__ import unicode_literals

from django.db import models
from utils.sales import TransactionEntityType


class Dealer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    ein = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def type(self):
    	return TransactionEntityType.dealer.value


    class Meta:
        ordering = ('created_at',)
