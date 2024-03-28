import datetime
import json
from io import StringIO

import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from bonds.models import Bond
from securitieswebsite import settings
from shares.models import Share
from .models import UserPreference
from .tasks import create_pdf, create_excel, create_json
from .utils import parse_bonds_json, parse_shares_json, add_securities

redis_exchange = getattr(settings, 'EXCHANGE')


@login_required(login_url='/authentication/login')
def index(request):
    user_preferences = UserPreference.objects.filter(user=request.user)
    paginator = Paginator(user_preferences, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'preferences/index.html', context)


@login_required(login_url='/authentication/login')
def show_user_preferences(request):
    user_preferences = UserPreference.objects.filter(user=request.user).values()
    return JsonResponse(list(user_preferences), safe=False)


@login_required(login_url='/authentication/login')
def create_preference(request):
    if request.method == 'GET':
        return render(request, 'preferences/add.html', {"exchange": request.GET["pos"]})

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        if UserPreference.objects.filter(name=name, user=request.user).exists():
            messages.error(request, f'A set named "{name}" already exists!')
            return redirect('create-preference')

        user_preference = UserPreference.objects.create(name=name, description=description, user=request.user)

        if request.POST["exchange"]:
            res = redis_exchange.json().get(request.user.username, f'$[{request.POST['exchange']}].pref')
            securities = json.loads(*res)
            bonds_list = parse_bonds_json(securities['Bonds'])
            shares_list = parse_shares_json(securities['Shares'])
            add_securities(bonds_list, shares_list, user_preference)

        if request.POST.getlist('import'):
            file = request.FILES['file']
            if file.content_type.endswith('sheet'):
                bonds_df = pd.read_excel(file, 'Bonds', usecols=Bond.FIELDS)
                shares_df = pd.read_excel(file, 'Shares', usecols=Share.FIELDS)

                with StringIO() as io:
                    bonds_df.to_json(io, orient='records', date_format='iso', force_ascii=False, default_handler=str)
                    bonds_list = parse_bonds_json(json.loads(io.getvalue().strip()))
                    io.truncate(0)
                    io.seek(0)

                    shares_df.to_json(io, orient='records', date_format='iso', force_ascii=False, default_handler=str)
                    shares_list = parse_shares_json(json.loads(io.getvalue().strip()))
                    io.truncate(0)
                    io.seek(0)

            if file.content_type.endswith('json'):
                securities = json.load(file)
                bonds_list = parse_bonds_json(securities['Bonds'])
                shares_list = parse_shares_json(securities['Shares'])

            add_securities(bonds_list, shares_list, user_preference)

        messages.success(request, f'Set "{name}" has been successfully created')
        return redirect('preferences')


@login_required(login_url='/authentication/login')
def delete_preference(request, name):
    user_preference = UserPreference.objects.get(user=request.user, slug=name)

    for bond in user_preference.bonds.all():
        Bond.objects.get(name=bond.name).delete()

    for share in user_preference.shares.all():
        Share.objects.get(ticker=share.ticker).delete()

    user_preference.delete()

    messages.success(request, f'Set "{name}" successfully deleted')
    return redirect('preferences')


@login_required(login_url='/authentication/login')
def preference_details(request, name):
    user_preference = UserPreference.objects.get(user=request.user, slug=name)

    context = {
        'name': name,
        'bonds': user_preference.bonds.all().select_related('company'),
        'shares': user_preference.shares.all().select_related('company')
    }
    return render(request, 'preferences/details.html', context)


@login_required(login_url='/authentication/login')
def delete_bond(request, name, bond_pk):
    bond = Bond.objects.get(pk=bond_pk)

    user_preference = UserPreference.objects.get(user=request.user, slug=name)
    user_preference.bonds.remove(bond)
    bond.delete()

    messages.success(request, f'The bond has been successfully removed from set "{name}"')
    return redirect('preference-details', name)


@login_required(login_url='/authentication/login')
def delete_share(request, name, share_pk):
    share = Share.objects.get(pk=share_pk)

    user_preference = UserPreference.objects.get(user=request.user, slug=name)
    user_preference.shares.remove(share)
    share.delete()

    messages.success(request, f'The share has been successfully removed from set "{name}"')
    return redirect('preference-details', name)


def export_json(request, name):
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename={name}_' + \
                                      str(datetime.datetime.now()) + '.json'

    user_preference = UserPreference.objects.get(user=request.user, slug=name)

    response.write(create_json(user_preference))
    return response


def export_pdf(request, name):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; attachment; filename={name}_' + \
                                      str(datetime.datetime.now()) + '.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    user_preference = UserPreference.objects.get(user=request.user, slug=name)

    response.write(create_pdf(user_preference))
    return response


def export_excel(request, name):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={name}_' + \
                                      str(datetime.datetime.now()) + '.xlsx'

    user_preference = UserPreference.objects.get(user=request.user, slug=name)

    response.write(create_excel(user_preference))
    return response
