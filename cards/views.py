from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card
from orgs.models import Org
from cards.serializers import CardSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.template import loader
from users.models import UserCustom
from .forms import CardForm
import json

# Create your views here.


@login_required(login_url='../login/')
def listCards(request):
    if request.method=="GET":
        response = {}
        form = CardForm()
        template = loader.get_template('list_cards.html')
        user =UserCustom.objects.get(user_id__exact=request.user.pk)
        if user.org is None:
            return HttpResponse(template.render(response, request))
        if "deleted" in request.GET:
            cards = Card.objects.filter(org__exact=user.org)
        else:
            cards = Card.objects.filter(org__exact=user.org, deleted__exact='n')
        if "search" in request.GET:
            phrase = request.GET["search"]
            try:
                a = int(phrase)
                is_digit = True
            except:
                is_digit = False
            if is_digit:
                cards = cards.filter(code__exact=phrase)
            else:
                cards = cards.filter(holder_name__contains=phrase)
        if cards is not None:
            response = {"cards": cards, "form": form}
            return HttpResponse(template.render(response, request))


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
                        data = {
                            "code": card.code,
                            "holder_name": card.holder_name,
                            "accumulation" : card.accumulation,
                            "bonus": card.bonus,
                            "discount": card.discount

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


