from . import views
from django.urls import path

exchange_patterns = [
    path('', views.exchange, name="exchange"),
    path('send', views.send_preference, name="send_pref"),
    path('del', views.del_pref_from_inbox, name="del_prop"),
    path('show', views.show_pref_from_inbox, name="show_prop")
]
