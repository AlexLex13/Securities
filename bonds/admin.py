from django.contrib import admin
from .models import Bond


class BondAdmin(admin.ModelAdmin):
    list_display = ('name', 'maturity_years', 'profitability', 'coupon_yield',
                    'coupon_yield_last', 'rating', 'volume', 'coupon_value',
                    'coupon_payments_frequency', 'accumulated_income', 'duration',
                    'price', 'next_coupon_date', 'issue_date', 'maturity_date',
                    'offer_date', 'company')

    search_fields = ('name', 'issue_date', 'company',)

    list_per_page = 5


admin.site.register(Bond, BondAdmin)

