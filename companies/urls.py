from django.urls import path

from .views import CompaniesView

urlpatterns = [
    path('', CompaniesView.as_view(), name="companies"),
]
