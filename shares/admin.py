from django.contrib import admin

from shares.models import Share


class ShareAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'last_price', 'price_change', 'volume',
                    'last_transaction_time', 'weekly_price_change', 'monthly_price_change',
                    'annual_price_change', 'capitalization', 'volume_change', 'company')

    search_fields = ('name', 'ticker', 'company',)

    list_per_page = 5

admin.site.register(Share, ShareAdmin)
