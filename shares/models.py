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
    company = models.OneToOneField(to=Company, on_delete=models.CASCADE)

    objects = models.Manager()

    FIELDS = [
        'name', 'ticker', 'last_price', 'price_change', 'volume',
        'last_transaction_time', 'weekly_price_change', 'monthly_price_change',
        'annual_price_change', 'capitalization', 'volume_change', 'company'
    ]

    def get_fields(self):
        return [
            self.name, self.ticker, self.last_price, self.price_change,
            self.volume, self.last_transaction_time, self.weekly_price_change,
            self.monthly_price_change, self.annual_price_change,
            self.capitalization, self.volume_change, self.company.name
        ]

    def __str__(self):
        return self.name

    class Meta:
        ordering: ['name']

