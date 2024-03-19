from django.urls import path

from .views import CompaniesView, CompanyDetailView, BrokersView, BrokerDetailView

urlpatterns = [
    path('', CompaniesView.as_view(), name="companies"),
    path('<slug:slug>/', CompanyDetailView.as_view(), name="company_details"),
    path('<slug:slug>/', BrokerDetailView.as_view(), name="broker_details"),
    path('brokers', BrokersView.as_view(), name="brokers"),
]
