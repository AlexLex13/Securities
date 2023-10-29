import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from userpreferences.models import UserPreference
from .models import Bond


def search_bonds(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        bonds = Bond.objects.filter(name__icontains=search_str)

        data = bonds.values()
        return JsonResponse(list(data), safe=False)


def index(request):
    bonds = Bond.objects.all().select_related('company')
    paginator = Paginator(bonds, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'bonds/index.html', context)


@login_required(login_url='/authentication/login')
def add_bond(request, pk):
    preferences = UserPreference.objects.filter(user=request.user)

    if not preferences.exists():
        messages.error(request, "You don't have a single set. Create it in your profile!")
        return redirect('bonds')

    if request.method == 'POST':
        name = request.POST['name']

        bond = Bond.objects.get(pk=pk)

        selected_preference = preferences.get(name=name)

        if selected_preference.bonds.contains(bond):
            messages.info(request, f'The bond has already been added to set "{name}"')
            return redirect('bonds')

        selected_preference.bonds.add(bond)
        messages.success(request, f'The bond has been successfully added to set "{name}"')
        return redirect('bonds')
