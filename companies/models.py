from django.db import models
from djmoney.models.fields import MoneyField


class Company(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    industry = models.CharField(max_length=256)
    share_capital = MoneyField(max_digits=16, decimal_places=2, default_currency='USD')
    stock_market = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=256, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'
        ordering: ['name']


class Broker(models.Model):
    name = models.CharField(max_length=255)
    active_clients_number = models.PositiveIntegerField()
    stock_market = models.CharField(max_length=256, null=True, blank=True)
    trading_turnover = MoneyField(max_digits=16, decimal_places=2, default_currency='USD')
    equity_capital = MoneyField(max_digits=16, decimal_places=2, default_currency='USD')
    description = models.TextField(null=True, blank=True)
    website = models.CharField(max_length=256, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering: ['name']

    def __str__(self):
        return self.name
