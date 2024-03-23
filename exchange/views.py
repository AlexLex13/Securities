from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from securitieswebsite import settings
from userpreferences.models import UserPreference
from userpreferences.tasks import create_json

redis_exchange = getattr(settings, 'EXCHANGE')


@login_required(login_url='/authentication/login')
def exchange(request):
    arr = []
    arr.append(redis_exchange.hgetall(request.user.username))

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
        sender_name = request.POST['sender_name']
        description = request.POST['description']
        pref = request.POST['pref_name']
        print(sender_name, name, description, pref)

        preference = UserPreference.objects.get(user=request.user, name=pref)

        redis_exchange.hset(name, mapping={
            "sender": sender_name,
            "description": description,
            "pref": create_json(preference)
        })

        return redirect('exchange')
