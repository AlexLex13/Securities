from django.views.decorators.csrf import csrf_exempt

from . import views
from django.urls import path, include

preference_patterns = [
    path('', views.preference_details, name="preference-details"),
    path('del_bond/<int:bond_pk>', views.delete_bond, name="delete-bond"),
    path('del_share/<int:share_pk>', views.delete_share, name="delete-share"),
    path('export_csv', views.export_csv, name="export-csv"),
    path('export_pdf', views.export_pdf, name="export-pdf"),
]

urlpatterns = [
    path('', views.index, name="preferences"),
    path('delete/<str:name>', views.delete_preference, name="delete-preference"),
    path('add', views.create_preference, name="create-preference"),
    path('show_user_pref', csrf_exempt(views.show_user_preferences), name="show-user-preferences"),
    path('<str:name>/', include(preference_patterns)),
]
