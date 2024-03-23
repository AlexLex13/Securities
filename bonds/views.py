import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from companies.models import Company
from securitieswebsite import settings
from userpreferences.models import UserPreference
from .models import Bond
from .tasks import fetch_bonds, processing_bonds

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def index(request):
    bonds = fetch_bonds()
    paginator = Paginator(bonds, 15)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'bonds/index.html', context)


def search_bonds(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        bonds = Bond.objects.filter(name__icontains=search_str)

        data = bonds.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def add_bond(request, bond_name):
    preferences = UserPreference.objects.filter(user=request.user)

    if not preferences.exists():
        messages.error(request, "You don't have a single set. Create it in your profile!")
        return redirect('bonds')

    if request.method == 'POST':
        name = request.POST['ref_name']

        selected_preference = preferences.get(name=name)

        if len(selected_preference.bonds.filter(slug=bond_name)):
            messages.info(request, f'The bond has already been added to set "{name}"')
            return redirect('bonds')

        bond_fields = processing_bonds(request.POST['fields'])
        dct = dict(zip(Bond.FIELDS, bond_fields[:-2]))

        if len(Bond.objects.filter(slug=bond_name)):
            Bond.objects.filter(slug=bond_name).update(**dct)
            return redirect('bonds')

        company = Company.objects.update_or_create(name=bond_fields[-2])

        bond = Bond.objects.update_or_create(**dct, company=company[0])
        selected_preference.bonds.add(bond[0])

        messages.success(request, f'The bond has been successfully added to set "{name}"')
        return redirect('bonds')
