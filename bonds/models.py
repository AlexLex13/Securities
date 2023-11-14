from django.db import models
from djmoney.models.fields import MoneyField
from companies.models import Company


class Bond(models.Model):
    name = models.CharField(max_length=256)
    maturity_years = models.FloatField()
    profitability = models.FloatField()
    coupon_yield = models.FloatField()
    coupon_yield_last = models.FloatField(null=True, blank=True)
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

    FIELDS = [
        'name', 'maturity_years', 'profitability', 'coupon_yield',
        'coupon_yield_last', 'rating', 'volume', 'coupon_value',
        'coupon_payments_frequency', 'accumulated_income', 'duration',
        'price', 'next_coupon_date', 'issue_date', 'maturity_date',
        'offer_date', 'company'
    ]

    def get_fields(self):
        return [
            self.name, self.maturity_years, self.profitability, self.coupon_yield,
            self.coupon_yield_last, self.rating, self.volume, self.coupon_value,
            self.coupon_payments_frequency, self.accumulated_income, self.duration,
            self.price, self.next_coupon_date, self.issue_date,
            self.maturity_date, self.offer_date, self.company.name
        ]

    def __str__(self):
        return self.name

    class Meta:
        ordering: ['name']
