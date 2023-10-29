from django.db import models
from djmoney.models.fields import MoneyField
from companies.models import Company


class Share(models.Model):
    name = models.CharField(max_length=256)
    ticker = models.CharField(max_length=10, unique=True)
    last_price = MoneyField(max_digits=9, decimal_places=2, default_currency='USD', null=True, blank=True)
    price_change = models.FloatField()
    volume = MoneyField(max_digits=16, decimal_places=2, default_currency='USD')
    last_transaction_time = models.TimeField()
    weekly_price_change = models.FloatField()
    monthly_price_change = models.FloatField(null=True, blank=True)
    annual_price_change = models.FloatField(null=True, blank=True)
    capitalization = MoneyField(max_digits=16, decimal_places=2, default_currency='USD')
    volume_change = models.FloatField()
    company = models.OneToOneField(to=Company, on_delete=models.CASCADE, primary_key=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering: ['name']

