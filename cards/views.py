from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.db.models import Q
from cards.models import Card
from orgs.models import Org
from django.contrib.auth.decorators import login_required
from django.template import loader
from users.models import UserCustom
from .forms import CardForm, MassCardForm
import json
from datetime import datetime
from django.db import transaction

# Create your views here.

def is_digit(a):
    try:
        b = int(a)
        return True
    except:
        return False



@login_required(login_url='../login/')
def listCards(request):
    if request.method=="GET":
        response = {}
        form = CardForm()
        template = loader.get_template('list_cards.html')
        response = {"add_form": form, "mass_add_form": MassCardForm()}
        return HttpResponse(template.render(response, request))

    if request.method == "POST":
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        q = Q(org_id__exact=user.org.pk)
        data = None
        selection_parameters = None
        post = request.POST
        if "cmd" in post:
            if post["cmd"] == "update":
                if "data" in post:
                    data = json.loads(post["data"])
                if "selection_parameters" in post:
                    selection_parameters = json.loads(post["selection_parameters"])
                if selection_parameters is not None:
                    if selection_parameters["deleted"] == "n" or selection_parameters["deleted"] == "":
                        q &= Q(deleted__exact='n')
                    if is_digit(selection_parameters["search"]):
                        q &= Q(code__startswith=selection_parameters["search"])
                    elif selection_parameters["search"] != '':
                        q &= Q(holder_name__contains=selection_parameters["search"])
                total = Card.objects.filter(q).count()
                if data["count"] > total:
                    data["count"] = total
                cards = Card.objects.filter(q).order_by(selection_parameters["sort"]).all()[data["start"]:data["start"]+data["count"]]
                resp_cards=[]
                for card in cards:
                    resp_cards.append(
                        {
                            "code": card.code,
                            'holder_name': card.holder_name,
                            'type': card.get_type(),
                            'deleted': card.deleted,
                        }
                    )

                response = {"result": "ok", "data": resp_cards, "total": total}
                return HttpResponse(json.dumps(response), content_type="application/json")



@login_required(login_url='./login/')
def maintenance(request):
    response = {}
    if request.method=="POST":
        post = request.POST
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        if "cmd" in post:
            if post["cmd"] == "save":  # сохранение карты
                if "data" in post:
                    data = json.loads(post["data"])
                    try:
                        form = CardForm(data)
                        if form.is_valid():
                            try:
                                card = Card.objects.get(code__exact=form.cleaned_data['code'])
                            except ObjectDoesNotExist as e:
                                card = Card()
                            card.code = form.cleaned_data['code']
                            card.holder_name = form.cleaned_data['holder_name']
                            card.bonus = form.cleaned_data['bonus']
                            card.discount = form.cleaned_data['discount']
                            card.accumulation = form.cleaned_data['accumulation']
                            card.type = form.cleaned_data['type']
                            card.changes_date = datetime.now().date()
                            if not card.reg_date:
                                card.reg_date = datetime.now().date()
                                card.last_transaction_date = datetime.now().date()
                            card.org=user.org
                            card.save()
                            response = {"result": "ok"}
                            return HttpResponse(json.dumps(response), content_type="application/json")
                    except:
                        response = {"result": "error"}
                        return HttpResponse(json.dumps(response), content_type="application/json")
            if post["cmd"] == "get":  # получение данных по карте
                if "data" in post:
                    data = json.loads(post["data"])
                    try:
                        card = Card.objects.filter(code__exact=data["code"],
                                                   org_id__exact=user.org.pk
                                                   ).get()

                        date_func = lambda a: '' if a is None else a.strftime('%Y-%m-%d')
                        data = {
                            "code": card.code,
                            "holder_name": card.holder_name,
                            "accumulation" : card.accumulation,
                            "bonus": card.bonus,
                            "discount": card.discount,
                            "type": card.type,
                            "reg_date": date_func(card.reg_date),
                            "changes_date": date_func(card.changes_date),
                            "last_transaction_date": date_func(card.last_transaction_date)

                        }
                        response = {"result": "ok", "data": data}
                        response = json.dumps(response)
                        return HttpResponse(response, content_type="application/json")
                    except Exception as err:
                        response = {"result": "error", "msg": err}
                        return HttpResponse(json.dumps(response), content_type="application/json")
            if post["cmd"] == "delete":  # получение данных по карте
                if "data" in post:
                    data = json.loads(post["data"])
                    try:
                        for code in data:
                            card = Card.objects.filter(code__exact=code,
                                                   org_id__exact=user.org.pk
                                                   ).get()
                            card.deleted = 'y'
                            card.save()
                        response = {"result": "ok", "data": data}
                        response = json.dumps(response)
                        return HttpResponse(response, content_type="application/json")
                    except Exception as err:
                        response = {"result": "error", "msg": err}
                        return HttpResponse(json.dumps(response), content_type="application/json")
            if post["cmd"] == "restore":  # получение данных по карте
                if "data" in post:
                    data = json.loads(post["data"])
                    try:
                        for code in data:
                            card = Card.objects.filter(code__exact=code,
                                                       org_id__exact=user.org.pk
                                                       ).get()
                            card.deleted = 'n'
                            card.save()
                        response = {"result": "ok", "data": data}
                        response = json.dumps(response)
                        return HttpResponse(response, content_type="application/json")
                    except Exception as err:
                        response = {"result": "error", "msg": err}
                        return HttpResponse(json.dumps(response), content_type="application/json")


@transaction.atomic
@login_required(login_url='./login/')
def mass_add(request):
    if request.method == "POST":
        data = request.POST
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        try:
            form = MassCardForm(data)
            if form.is_valid():
                start = form.cleaned_data['code_start']
                end = form.cleaned_data['code_end']
                length = form.cleaned_data['code_length']
                pool = [str(x).zfill(length) for x in range(start, end+1, 1)]
                for code in pool:
                    try:
                        card = Card.objects.get(code__exact=code, org_id__exact=user.org.pk)
                        exist = True
                    except:
                        card = Card()
                        exist = False

                    card.org = user.org

                    if not exist:
                        card.code = code
                        card.org = user.org
                        card.type = form.cleaned_data['type']
                        card.discount = form.cleaned_data['discount']
                        card.bonus = form.cleaned_data['bonus']
                        card.accumulation = form.cleaned_data['accumulation']
                        card.reg_date = datetime.now().date()
                        card.last_transaction_date = datetime.now().date()

                    else:
                        if form.cleaned_data['doubles'] == 'rewrite':
                            card.type = form.cleaned_data['type']
                            card.discount = form.cleaned_data['discount']
                            card.bonus = form.cleaned_data['bonus']
                            card.accumulation = form.cleaned_data['accumulation']
                            card.fio = ''
                            card.deleted = 'n'
                            card.reg_date = datetime.now().date()
                            card.last_transaction_date = datetime.now().date()
                            card.changes_date = None
                        elif form.cleaned_data['doubles'] == 'append':
                            card.type = form.cleaned_data['type']
                            card.discount = form.cleaned_data['discount']
                            card.bonus = form.cleaned_data['bonus']
                            card.accumulation = form.cleaned_data['accumulation']
                            card.deleted = 'n'
                            card.reg_date = datetime.now().date()
                            card.last_transaction_date = datetime.now().date()
                            card.changes_date = None
                        elif form.cleaned_data['doubles'] == 'ignore':
                            continue
                    card.save()

                return HttpResponseRedirect('/cards/')
        except Exception as e:
            response = {"result": e}
            return HttpResponse(response, content_type="application/json")

        response = {"result": "error"}
        return HttpResponse(json.dumps(response), content_type="application/json")


