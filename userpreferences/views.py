import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from bonds.models import Bond
from shares.models import Share
from .models import UserPreference
from .tasks import create_csv


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
        return render(request, 'preferences/add.html')

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']

        if UserPreference.objects.filter(name=name, user=request.user).exists():
            messages.error(request, f'A set named "{name}" already exists!')
            return redirect('create-preference')

        UserPreference.objects.create(name=name, description=description, user=request.user)

        messages.success(request, f'Set "{name}" has been successfully created')
        return redirect('preferences')


@login_required(login_url='/authentication/login')
def delete_preference(request, name):
    UserPreference.objects.filter(user=request.user, name=name).delete()

    messages.success(request, f'Set "{name}" successfully deleted')
    return redirect('preferences')


@login_required(login_url='/authentication/login')
def preference_details(request, name):
    user_preference = UserPreference.objects.get(user=request.user, name=name)

    context = {
        'name': name,
        'bonds': user_preference.bonds.all(),
        'shares': user_preference.shares.all()
    }
    return render(request, 'preferences/details.html', context)


@login_required(login_url='/authentication/login')
def delete_bond(request, name, bond_pk):
    bond = Bond.objects.get(pk=bond_pk)

    user_preference = UserPreference.objects.get(user=request.user, name=name)
    user_preference.bonds.remove(bond)

    messages.success(request, f'The bond has been successfully removed from set "{name}"')
    return redirect('preference-details', name)


@login_required(login_url='/authentication/login')
def delete_share(request, name, share_pk):
    share = Share.objects.get(pk=share_pk)

    user_preference = UserPreference.objects.get(user=request.user, name=name)
    user_preference.shares.remove(share)

    messages.success(request, f'The share has been successfully removed from set "{name}"')
    return redirect('preference-details', name)


def export_csv(request, name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Securities_' + \
                                      str(datetime.datetime.now()) + '.csv'

    user_preference = UserPreference.objects.get(user=request.user, name=name)

    create_csv(response, user_preference)

    return response
