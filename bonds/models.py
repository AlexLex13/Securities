from django.db import models
from djmoney.models.fields import MoneyField
from companies.models import Company


class Bond(models.Model):
    name = models.CharField(max_length=256)
    maturity_years = models.FloatField()
    profitability = models.FloatField()
    coupon_yield = models.FloatField()
    coupon_yield_last = models.FloatField()
    rating = models.CharField(max_length=4, null=True, blank=True)
    volume = MoneyField(max_digits=16, decimal_places=2, default_currency='USD')
    coupon_value = MoneyField(max_digits=5, decimal_places=2, default_currency='USD')
    coupon_payments_frequency = models.FloatField()
    accumulated_income = MoneyField(max_digits=5, decimal_places=2, default_currency='USD', null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)
    price = MoneyField(max_digits=5, decimal_places=2, default_currency='USD')
    next_coupon_date = models.DateField()
    issue_date = models.DateField()
    maturity_date = models.DateField()
    offer_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering: ['name']
