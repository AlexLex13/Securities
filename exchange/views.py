import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from securitieswebsite import settings
from userpreferences.models import UserPreference
from userpreferences.tasks import create_json

redis_exchange = getattr(settings, 'EXCHANGE')


@login_required(login_url='/authentication/login')
def exchange(request):
    arr = redis_exchange.json().get(request.user.username)

    if not arr:
        arr = []

    paginator = Paginator(arr, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'exchange/index.html', context)


@login_required(login_url='/authentication/login')
def send_preference(request):
    if request.method == 'GET':
        return render(request, 'exchange/send.html')

    if request.method == 'POST':
        name = request.POST['name']
        if not User.objects.filter(username=name).exists():
            messages.error(request, f"User {name} doesn't exists!")
            return redirect('exchange')

        description = request.POST['description']
        pref = request.POST['pref_name']

        preference = UserPreference.objects.get(user=request.user, name=pref)

        if not redis_exchange.json().get(name):
            redis_exchange.json().set(name, '$', [])

        redis_exchange.json().arrappend(name, '$', {
            "sender": request.user.username,
            "description": description,
            "pref": create_json(preference)
        })

        return redirect('exchange')


@login_required(login_url='/authentication/login')
def del_pref_from_inbox(request):
    redis_exchange.json().arrpop(request.user.username, '$', request.GET['pos'])
    return redirect('exchange')


@login_required(login_url='/authentication/login')
def show_pref_from_inbox(request):
    res = redis_exchange.json().get(request.user.username, f'$[{request.GET['pos']}].pref')
    securities = json.loads(*res)
    context = {
        'position': request.GET['pos'],
        'bonds': securities["Bonds"],
        'shares': securities["Shares"],
    }
    return render(request, 'exchange/show.html', context)
