from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from rest_framework.request import Request

from cards.models import Card
from django.contrib.auth.decorators import login_required
from django.template import loader
from users.models import UserCustom
from .forms import CardForm, MassCardForm
import json
from datetime import datetime
from django.db import transaction
from .serializers import CardSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.

def is_digit(a):
    try:
        b = int(a)
        return True
    except:
        return False



@login_required(login_url='/login/')
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
                    if selection_parameters["type"] != "":
                        q &= Q(type__exact=selection_parameters["type"])
                    if is_digit(selection_parameters["search"]):
                        q &= Q(code__startswith=selection_parameters["search"])
                    elif selection_parameters["search"] != '':
                        q &= Q(holder_name__contains=selection_parameters["search"])
                    if "order" in selection_parameters:
                        order = selection_parameters["order"]
                    else:
                        order = '-'
                total = Card.objects.filter(q).count()
                if data["count"] > total:
                    data["count"] = total
                cards = Card.objects.filter(q).order_by(order+selection_parameters["sort"]).all()[data["start"]:data["start"]+data["count"]]
                resp_cards = []
                for card in cards:
                    resp_cards.append(
                        {
                            "code": card.code,
                            'holder_name': card.holder_name,
                            'accumulation': card.accumulation,
                            'type': card.get_type(),
                            'deleted': card.deleted,
                        }
                    )

                response = {"result": "ok", "data": resp_cards, "total": total}
                return HttpResponse(json.dumps(response), content_type="application/json")



@login_required(login_url='/login/')
def maintenance(request):
    response = {}
    if request.method == "POST":
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
                                #if "collision" in post:
                                    #if post['collision']
                                card = Card.objects.get(code__exact=form.cleaned_data['code'], org_id__exact=user.org.pk)

                            except ObjectDoesNotExist as e:
                                card = Card()
                            card.code = form.cleaned_data['code']
                            card.holder_name = form.cleaned_data['holder_name']
                            card.holder_phone = form.cleaned_data['holder_phone']
                            card.bonus = form.cleaned_data['bonus']
                            card.discount = form.cleaned_data['discount']
                            card.accumulation = form.cleaned_data['accumulation']
                            card.type = form.cleaned_data['type']
                            card.changes_date = datetime.now().date()
                            if not card.reg_date:
                                card.reg_date = datetime.now().date()
                                card.last_transaction_date = datetime.now().date()
                            card.org = user.org
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
                            "holder_phone": card.holder_phone,
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
@login_required(login_url='/login/')
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


# REST VIEWS

@login_required(login_url='/login/')
@csrf_exempt
def rest_cards_list(request):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        cards = Card.objects.filter(org_id__exact=user.org.pk)[:100]

        serializer_context = {
            'request': Request(request),
        }

        serializer = CardSerializer(cards, many=True, context=serializer_context)

        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        data = json.loads(request.body.decode())
        if ('current' in data) and ("count" in data):
            try:
                current = int(data['current'])
                count = int(data['count'])
            except:
                current = 0
                count = 50
        else:
            current = 0
            count = 50

        total = Card.objects.filter(org_id__exact=user.org.pk).count()

        cards = Card.objects.filter(org_id__exact=user.org.pk)[current:current+count]

        serializer_context = {
            'request': Request(request),
        }

        serializer = CardSerializer(cards, many=True, context=serializer_context)
        response["data"] = serializer.data
        response["list_current_position"] = current
        response["list_total"] = total

        return JsonResponse(response, safe=False)

@csrf_exempt
@login_required(login_url='/login/')
def rest_card_by_code(request, card_code):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        try:
            card = Card.objects.get(org_id__exact=user.org.pk, code__exact=card_code)
        except:
            return HttpResponse(status=404)

        serializer_context = {
            'request': Request(request),
        }

        serializer = CardSerializer(card, many=False, context=serializer_context)

        response = serializer.data
        response['bonuses'] = card.get_bonuses_array()
        response['bonus'] = card.get_total_bonus()
        return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        card_new_data = json.loads(request.body.decode())
        try:
            card = Card.objects.get(org_id__exact=user.org.pk, code__exact=card_code)
        except:
            return HttpResponse(status=404)

        serializer_context = {
            'request': Request(request),
        }
        serializer = CardSerializer(card, data=card_new_data)
        if serializer.is_valid():
            serializer.save()
            response['status'] = 'success'
            response['message'] = 'Карта с кодом %s успешно сохранена!' % card_code
            return JsonResponse(response, safe=False)
        response['status'] = 'error'
        response['message'] = str(serializer.errors)
        return JsonResponse(response, status=400)