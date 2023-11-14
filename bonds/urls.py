from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="bonds"),
    path('add/<str:bond_name>', views.add_bond, name="add-bond"),
    path('search_bonds', csrf_exempt(views.search_bonds), name="search-bonds"),
]
