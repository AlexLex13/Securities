from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views
from .views import SharesView

urlpatterns = [
    path('', SharesView.as_view(), name="shares"),
    path('add/<int:pk>', views.add_share, name="add-share"),
    path('search_shares', csrf_exempt(views.search_shares), name="search-shares")
]
