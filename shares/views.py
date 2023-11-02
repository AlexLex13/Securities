import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from userpreferences.models import UserPreference
from .models import Share


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class SharesView(ListView):
    template_name = 'shares/index.html'
    context_object_name = 'shares'
    paginate_by = 5

    def get_queryset(self):
        return Share.objects.all().select_related('company')


def search_shares(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        shares = Share.objects.filter(
            Q(name__icontains=search_str) |
            Q(ticker__icontains=search_str))

        data = shares.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def add_share(request, pk):
    preferences = UserPreference.objects.filter(user=request.user)

    if not preferences.exists():
        messages.error(request, "You don't have a single set. Create it in your profile!")
        return redirect('shares')

    if request.method == 'POST':
        name = request.POST['name']

        share = Share.objects.get(pk=pk)

        selected_preference = preferences.get(name=name)

        if selected_preference.shares.contains(share):
            messages.info(request, f'The share has already been added to set "{name}"')
            return redirect('shares')

        selected_preference.shares.add(share)
        messages.success(request, f'The share has been successfully added to set "{name}"')
        return redirect('shares')
