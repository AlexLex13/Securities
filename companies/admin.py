from django.contrib import admin

from companies.models import Company, Broker


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'industry', 'share_capital',
                    'stock_market', 'description', 'website',)

    search_fields = ('name', 'country', 'industry',)

    list_per_page = 5


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', 'active_clients_number', 'stock_market',
                    'trading_turnover', 'equity_capital',
                    'description', 'website',)

    search_fields = ('name',)

    list_per_page = 5

admin.site.register(Company, CompanyAdmin)
admin.site.register(Broker, BrokerAdmin)
