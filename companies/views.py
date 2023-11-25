from django.shortcuts import render
from django.views.generic import ListView, DetailView

from companies.models import Company, Broker
from companies.tasks import fetch_brokers


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


class BrokersView(ListView):
    template_name = 'companies/bk_index.html'
    context_object_name = 'brokers'
    paginate_by = 10

    def get_queryset(self):
        return fetch_brokers()

