import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView

from companies.models import Company
from userpreferences.models import UserPreference
from .models import Share
from .tasks import fetch_shares, processing_shares


class SharesView(ListView):
    template_name = 'shares/index.html'
    context_object_name = 'shares'
    paginate_by = 15

    def get_queryset(self):
        return fetch_shares()


def search_shares(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        shares = Share.objects.filter(
            Q(name__icontains=search_str) |
            Q(ticker__icontains=search_str))

        data = shares.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def add_share(request, ticker):
    preferences = UserPreference.objects.filter(user=request.user)

    if not preferences.exists():
        messages.error(request, "You don't have a single set. Create it in your profile!")
        return redirect('shares')

    if request.method == 'POST':
        name = request.POST['ref_name']

        selected_preference = preferences.get(name=name)

        if len(selected_preference.shares.filter(ticker=ticker)):
            messages.info(request, f'The share has already been added to set "{name}"')
            return redirect('shares')

        share_fields = processing_shares(request.POST['fields'])
        dct = dict(zip(Share.FIELDS, share_fields[:-1]))

        if len(Share.objects.filter(ticker=ticker)):
            Share.objects.filter(ticker=ticker).update(**dct)
            return redirect('shares')

        company = Company.objects.update_or_create(name=share_fields[-1])

        share = Share(**dct, company=company[0])
        share.save()

        selected_preference.shares.add(share)
        messages.success(request, f'The share has been successfully added to set "{name}"')
        return redirect('shares')
