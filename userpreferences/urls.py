from django.views.decorators.csrf import csrf_exempt

from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name="preferences"),
    path('delete/<str:name>', views.delete_preference, name="delete-preference"),
    path('add', views.create_preference, name="create-preference"),
    path('show_user_pref', csrf_exempt(views.show_user_preferences), name="show-user-preferences"),
    path('<str:name>', views.preference_details, name="preference-details"),
    path('<str:name>/delete/<int:bond_pk>', views.delete_bond, name="delete-bond"),
    path('<str:name>/delete/<int:share_pk>', views.delete_share, name="delete-share"),
]
