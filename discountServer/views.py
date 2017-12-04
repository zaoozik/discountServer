import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext

from core.forms import BonusForm, DiscountForm, ComboForm, AlgorithmForm
from users.forms import CashBoxForm
from users.models import UserCustom, CashBox
from core.models import DiscountPlan




@login_required
def index(request):
    return render(request, 'main.html')


def signIn(request):
    response = {}
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
    if request.method == 'GET':
        response = {}
        template = loader.get_template('settings.html')
        return HttpResponse(template.render(response, request))


def settings_discount(request):
    if request.method == 'POST':
        if 'cmd' in request.POST:
            user = UserCustom.objects.get(user_id__exact=request.user.pk)
            d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
            response = {}
            if request.POST['cmd'] == 'get':
                initials = json.loads(d_plan.parameters)
                if d_plan.algorithm == 'bonus':
                    form = BonusForm(initial=initials)
                    alg_form = AlgorithmForm(initial={'algorithm': 'bonus'})
                elif d_plan.algorithm == 'discount':
                    form = DiscountForm()
                    alg_form = AlgorithmForm(initial={'algorithm': 'discount'})
                    response = {'rules': initials['rules']}
                elif d_plan.algorithm == 'combo':
                    form = ComboForm(initial=initials)
                    alg_form = AlgorithmForm(initial={'algorithm': 'combo'})
                    response = {'rules': initials['rules']}

                template = loader.get_template('settings_discount.html')
                html = template.render({'form': form,
                                        'alg_form': alg_form
                                        }, request)
                response.update({"html": html, "algorithm": d_plan.algorithm})
                return HttpResponse(json.dumps(response), content_type="application/json")
            if request.POST['cmd'] == 'update':
                if 'algorithm' in request.POST:
                    algorithm = request.POST['algorithm']
                    if algorithm == 'bonus':
                        form = BonusForm()
                        form.data['assume_delta'] = d_plan.time_delay
                        alg_form = AlgorithmForm(initial={'algorithm': 'bonus'})
                    if algorithm == 'discount':
                        form = DiscountForm()
                        alg_form = AlgorithmForm(initial={'algorithm': 'discount'})
                    if algorithm == 'combo':
                        form = ComboForm()
                        form.data['assume_delta'] = d_plan.time_delay
                        alg_form = AlgorithmForm(initial={'algorithm': 'combo'})
                    template = loader.get_template('settings_discount.html')
                    html = template.render({'form': form,
                                            'alg_form': alg_form
                                            }, request)
                    response = {"html": html, "algorithm": d_plan.algorithm}
                    return HttpResponse(json.dumps(response), content_type="application/json")
            if request.POST['cmd'] == 'save':
                if 'algorithm' in request.POST:
                    algorithm = request.POST['algorithm']
                    if 'data' in request.POST:
                        data = json.loads(request.POST['data'])
                        if algorithm == 'bonus':
                            form = BonusForm(data)
                            if form.is_valid():
                                try:
                                    d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                                except:
                                    d_plan = DiscountPlan()
                                d_plan.algorithm = algorithm
                                parameters = {
                                    'bonus_cost': form.cleaned_data['bonus_cost'],
                                    'max_bonus_percentage': form.cleaned_data['max_bonus_percentage'],
                                    'round': form.cleaned_data['round'],
                                    'min_transaction': form.cleaned_data['min_transaction'],
                                    'zeroing_delta': form.cleaned_data['zeroing_delta'],
                                }
                                d_plan.time_delay = form.cleaned_data['assume_delta']
                                d_plan.parameters = json.dumps(parameters)
                                d_plan.org = user.org
                                d_plan.save()
                                return redirect('/settings/')
                        elif algorithm == 'discount':
                            form = DiscountForm(data)
                            if form.is_valid():
                                try:
                                    d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                                except:
                                    d_plan = DiscountPlan()
                                d_plan.algorithm = algorithm
                                parameters = {
                                    'rules': data['rules']
                                }
                                d_plan.time_delay = 0
                                d_plan.parameters = json.dumps(parameters)
                                d_plan.org = user.org
                                d_plan.save()
                                return redirect('/settings/')

                        elif algorithm == 'combo':
                            form = ComboForm(data)
                            if form.is_valid():
                                try:
                                    d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                                except:
                                    d_plan = DiscountPlan()
                                d_plan.algorithm = algorithm
                                parameters = {
                                    'rules': data['rules'],
                                    'bonus_cost': form.cleaned_data['bonus_cost'],
                                    'max_bonus_percentage': form.cleaned_data['max_bonus_percentage'],
                                    'round': form.cleaned_data['round'],
                                    'min_transaction': form.cleaned_data['min_transaction'],
                                    'zeroing_delta': form.cleaned_data['zeroing_delta'],
                                }
                                d_plan.time_delay = form.cleaned_data['assume_delta']
                                d_plan.parameters = json.dumps(parameters)
                                d_plan.org = user.org
                                d_plan.save()

                                response = {"result": "ok"}
                                return redirect('/settings/')



def settings_workplace(request):
    if request.method == 'POST':
        if 'cmd' in request.POST:
            user = UserCustom.objects.get(user_id__exact=request.user.pk)
            d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
            response = {}
            if request.POST['cmd'] == 'get':
                template = loader.get_template('settings_workplace.html')
                html = template.render({'cashboxes': user.get_cashboxes,
                                        'licenses_count': user.licenses_count - user.count_cashboxes(),
                                        'form': CashBoxForm(),
                                        }, request)
                response.update({"html": html, "algorithm": d_plan.algorithm})
                return HttpResponse(json.dumps(response), content_type="application/json")
            if request.POST['cmd'] == 'save':
                if (user.licenses_count - user.count_cashboxes()) == 0:
                    response = {'result': 'error'}
                    return HttpResponse(json.dumps(response))
                if 'data' in request.POST:
                    data = request.POST
                    d_form = CashBoxForm(json.loads(data['data']))
                    if d_form.is_valid():
                        new_box = CashBox()
                        new_box.init_frontol_key()
                        new_box.user = user
                        new_box.address = d_form.cleaned_data['address']
                        new_box.serial_number = d_form.cleaned_data['serial_number']
                        new_box.name = d_form.cleaned_data['name']
                        new_box.save()
                        response = {'result': 'ok'}
                        return HttpResponse(json.dumps(response))
                response = {'result': 'error'}
                return HttpResponse(json.dumps(response))
            if request.POST['cmd'] == 'delete':
                if 'data' in request.POST:
                    data = json.loads(request.POST['data'])
                    if 'key' in data:
                        try:
                            cash = CashBox.objects.get(user_id__exact=user.pk, frontol_key__exact=data['key'])
                            cash.delete()
                            response = {'result': 'ok'}
                            return HttpResponse(json.dumps(response))
                        except Exception as e:
                            pass
                response = {'result': 'error'}
                return HttpResponse(json.dumps(response))

def settings_org(request):
    if request.method == 'POST':
        if 'cmd' in request.POST:
            user = UserCustom.objects.get(user_id__exact=request.user.pk)
            d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
            response = {}
            if request.POST['cmd'] == 'get':
                template = loader.get_template('settings_org.html')
                html = template.render({'org_name': user.org.name,
                                        'active': user.active_to
                                        }, request)
                response.update({"html": html, "algorithm": d_plan.algorithm})
                return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def settingsSave(request):
    if request.method == 'POST':
        if 'data' in request.POST:
            user = UserCustom.objects.get(user_id__exact=request.user.pk)
            data = json.loads(request.POST['data'])
            if data['algorithm'] == 'bonus':
                form = BonusForm(data)
                if form.is_valid():
                    try:
                        d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                    except:
                        d_plan = DiscountPlan()
                    d_plan.algorithm = form.cleaned_data['algorithm']
                    parameters = {
                        'bonus_cost': form.cleaned_data['bonus_cost'],
                        'max_bonus_percentage': form.cleaned_data['max_bonus_percentage'],
                        'round': form.cleaned_data['round'],
                        'min_transaction': form.cleaned_data['min_transaction'],
                        'zeroing_delta': form.cleaned_data['zeroing_delta'],
                    }
                    d_plan.time_delay = form.cleaned_data['assume_delta']
                    d_plan.parameters = json.dumps(parameters)
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
                    }
                    d_plan.time_delay = 0
                    d_plan.parameters=json.dumps(parameters)
                    d_plan.org = user.org
                    d_plan.save()
                    response = {'form': form, 'org_name': 'СОХРАНЕНО'}
                    template = loader.get_template('settings.html')
                    return redirect('/settings/')
            elif request.POST['algorithm'] == 'combo':
                form = ComboForm(request.POST)
                if form.is_valid():
                    try:
                        d_plan = DiscountPlan.objects.get(org_id__exact=user.org.pk)
                    except:
                        d_plan = DiscountPlan()
                    d_plan.algorithm = form.cleaned_data['algorithm']
                    parameters = {
                        'rules': form.cleaned_data['rules'],
                        'bonus_cost': form.cleaned_data['bonus_cost'],
                        'max_bonus_percentage': form.cleaned_data['max_bonus_percentage'],
                        'round': form.cleaned_data['round'],
                        'min_transaction': form.cleaned_data['min_transaction'],
                        'zeroing_delta': form.cleaned_data['zeroing_delta'],
                    }
                    d_plan.time_delay = form.cleaned_data['assume_delta']
                    d_plan.parameters=json.dumps(parameters)
                    d_plan.org = user.org
                    d_plan.save()
                    response = {'form': form, 'org_name': 'СОХРАНЕНО'}
                    template = loader.get_template('settings.html')
                    return redirect('/settings/')


@login_required
def exportFrontolSettings(request):
    if request.method == "GET":
        if 'KEY' in request.GET:
            cuser = UserCustom.objects.get(user_id__exact=request.user.pk)
            with open('D:/projects/discountServer\discountServer/static/documents/vti_discount.xch', 'r', encoding='cp1251') as set_file:
               buffer = set_file.read()
            str = 'var ACCESS_KEY = "%s";' % request.GET['KEY']
            buffer = buffer.replace('#ACCESS_KEY', str, 1)
            response = HttpResponse(buffer.encode(encoding='cp1251'), content_type="text/csv")
            response['Content-Disposition'] = 'attachment; filename="frontol_settings_%s.xch"' % cuser.user.username
            return response
