from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView

from companies.models import Company
from companies.tasks import fetch_brokers
from securitieswebsite import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL')


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class CompaniesView(ListView):
    template_name = 'companies/index.html'
    context_object_name = 'companies'
    paginate_by = 10

    def get_queryset(self):
        return Company.objects.all()


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/details.html'
    context_object_name = 'company'


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class BrokersView(ListView):
    template_name = 'companies/bk_index.html'
    context_object_name = 'brokers'
    paginate_by = 10

    def get_queryset(self):
        return fetch_brokers()
