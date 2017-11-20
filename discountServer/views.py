import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader
from core.forms import BonusForm, DiscountForm
from users.models import UserCustom
from core.models import DiscountPlan
from transactions.models import Transaction
from transactions.forms import ControlsForm



@login_required
def index(request):
    return render(request, 'main.html')


def signIn(request):
    response={}
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        post_data = request.POST
        if 'username' in post_data:
            try:
                user = User.objects.get(username=post_data['username'])
            except:
                response['result'] = 'error'
                response['msg'] = 'Пользователь не найден'
                return HttpResponse(json.dumps(response), content_type="application/json")
            if 'password' in post_data:
                user = authenticate(username=post_data['username'], password=post_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        response['result'] = 'ok'
                        response['msg'] = "Авторизация ок!"
                        return HttpResponse(json.dumps(response), content_type="application/json")
                    else:
                        response['result'] = 'error'
                        response['msg'] = "Пользователь не активен"
                        return HttpResponse(json.dumps(response), content_type="application/json")
                else:
                    response['result'] = 'error'
                    response['msg'] = 'Пароль введен неверно'
                    return HttpResponse(json.dumps(response), content_type="application/json")

        else:
            response['result'] = 'error'
            response['msg'] = 'Пароль не введен'
            return HttpResponse(json.dumps(response), content_type="application/json")

        #return HttpResponse(json.dumps({'answer': "POST"}), content_type="application/json")

@login_required
def signOff(request):
    logout(request)
    return redirect("/login/")

@login_required
def settings(request):
    if request.method=='GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        user.init_frontol_access_key()
        key = user.frontol_access_key
        user.save()
        add=''
        try:
            d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
            initials = json.loads(d_plan.parameters)
            initials.update({'algorithm': d_plan.algorithm})
            if d_plan.algorithm=='bonus':
                form = BonusForm(initials)
            if d_plan.algorithm == 'discount':
                form = DiscountForm(initials)
        except:
            form = BonusForm()
            add = '. Внимание! Сохраните настройки!'
        response = {'form': form, 'org_name': user.org.name + add, 'key': key, 'active': user.active_to}
        template = loader.get_template('settings.html')
        return HttpResponse(template.render(response, request))

    if request.method=='POST':
        if 'algorithm' in request.POST:
            user = UserCustom.objects.get(user_id__exact=request.user.pk)
            if request.POST['algorithm'] == 'bonus':
                form = BonusForm(initial={'algorithm': 'bonus'})
            elif request.POST['algorithm'] == 'discount':
                form = DiscountForm(initial={'algorithm': 'discount'})

            response = {'form': form, 'org_name': user.org.name}
            template = loader.get_template('settings.html')
            return HttpResponse(template.render(response, request))

@login_required
def settingsSave(request):
    if request.method=='POST':
        if 'algorithm' in request.POST:
            user = UserCustom.objects.get(user_id__exact=request.user.pk)
            if request.POST['algorithm'] == 'bonus':
                form = BonusForm(request.POST)
                if form.is_valid():
                    try:
                        d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                    except:
                        d_plan = DiscountPlan()
                    d_plan.algorithm = form.cleaned_data['algorithm']
                    parameters = {
                        'bonus_cost': form.cleaned_data['bonus_cost'],
                        'round': form.cleaned_data['round'],
                        'min_transaction': form.cleaned_data['min_transaction'],
                        'zeroing_delta': form.cleaned_data['zeroing_delta'],
                        'assume_delta': form.cleaned_data['assume_delta'],
                    }
                    d_plan.parameters=json.dumps(parameters)
                    d_plan.org = user.org
                    d_plan.save()
                    response = {'form': form, 'org_name': 'СОХРАНЕНО'}
                    template = loader.get_template('settings.html')
                    return redirect('/settings/')
            elif request.POST['algorithm'] == 'discount':
                form = DiscountForm(request.POST)
                if form.is_valid():
                    try:
                        d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                    except:
                        d_plan = DiscountPlan()
                    d_plan.algorithm = form.cleaned_data['algorithm']
                    parameters = {
                        'rules': form.cleaned_data['rules'],
                        'base_discount': form.cleaned_data['base_discount'],
                        'zeroing_delta': form.cleaned_data['zeroing_delta'],
                        'assume_delta': form.cleaned_data['assume_delta'],
                    }
                    d_plan.parameters=json.dumps(parameters)
                    d_plan.org = user.org
                    d_plan.save()
                    response = {'form': form, 'org_name': 'СОХРАНЕНО'}
                    template = loader.get_template('settings.html')
                    return redirect('/settings/')

@login_required
def exportFrontolSettings(request):
    if request.method=="GET":
        cuser = UserCustom.objects.get(user_id__exact=request.user.pk)
        with open('D:/projects/discountServer\discountServer/static/documents/vti_discount.xch', 'r', encoding='cp1251') as set_file:
           buffer = set_file.read()
        str = 'var ACCESS_KEY = "%s";' % cuser.frontol_access_key
        buffer = buffer.replace('#ACCESS_KEY', str, 1)
        response = HttpResponse(buffer.encode(encoding='cp1251'), content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="frontol_settings_%s.xch"' % cuser.user.username
        return response
