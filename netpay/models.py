from django.conf import settings
from django.db import models
import datetime


class Invoice_Netpay(models.Model):
    amount = models.DecimalField(default='0', max_digits=64, decimal_places=2)
    currency = models.CharField(max_length=3, blank=True, null=True)
    desc = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    accepted = models.DateTimeField(blank=True, null=True)
    end = models.BooleanField(default=False)
    login = models.CharField(max_length=128, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.datetime.now()
        return super(Invoice_Netpay, self).save(*args, **kwargs)

    class Meta:
        # managed = False
        db_table = "payments_netpay"
        verbose_name = ("Платёж Netpay")
        verbose_name_plural = ("Платежи Netpay")