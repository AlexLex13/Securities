import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from userpreferences.models import UserPreference
from .models import Bond
from .tasks import fetch_bonds, processing_fields


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

        if len(selected_preference.bonds.filter(name=bond_name)):
            messages.info(request, f'The bond has already been added to set "{name}"')
            return redirect('bonds')

        bond_fields = processing_fields(request.POST['fields'])

        dct = dict(zip(Bond.FIELDS, bond_fields))
        bond = Bond(**dct, company_id=1)
        bond.save()

        selected_preference.bonds.add(bond)
        messages.success(request, f'The bond has been successfully added to set "{name}"')
        return redirect('bonds')
