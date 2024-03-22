from django.views.decorators.csrf import csrf_exempt

from . import views
from django.urls import path, include

preference_patterns = [
    path('', views.preference_details, name="preference-details"),
    path('del', views.delete_preference, name="delete-preference"),
    path('del_bond/<int:bond_pk>', views.delete_bond, name="delete-bond"),
    path('del_share/<int:share_pk>', views.delete_share, name="delete-share"),
    path('export_json', views.export_json, name="export-json"),
    path('export_pdf', views.export_pdf, name="export-pdf"),
    path('export_excel', views.export_excel, name="export-excel"),
]

exchange_patterns = [
    path('', views.exchange, name="exchange"),

]

urlpatterns = [
    path('', views.index, name="preferences"),
    path('exchange/', include(exchange_patterns)),
    path('add', views.create_preference, name="create-preference"),
    path('show', csrf_exempt(views.show_user_preferences), name="show-user-preferences"),
    path('<slug:name>/', include(preference_patterns)),
]
