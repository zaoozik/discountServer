import json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Transaction
from django.contrib.auth.decorators import login_required
from users.models import UserCustom
from cards.models import Card
from cards.forms import CardForm
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.template import loader
from django.db.models import Q
from rest_framework.request import Request
from .serializers import TransactionSerializer
from core.models import Operations



# Create your views here.
@login_required
def listTrans(request):
    if request.method == "GET":
        response = {"card_form": CardForm()}
        template = loader.get_template('transactions.html')
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
                    if selection_parameters["type"]:
                        q &= Q(type__exact=selection_parameters["type"])
                    if selection_parameters["dateFrom"]:
                        q &= Q(date__date__gte=selection_parameters["dateFrom"])
                    if selection_parameters["dateTo"]:
                        q &= Q(date__date__lte=selection_parameters["dateTo"])
                    if selection_parameters["card"]:
                        try:
                            card_id = Card.objects.get(code__exact=selection_parameters["card"]).pk
                        except:
                            card_id =False
                        if card_id:
                            q &= Q(card_id__exact=card_id)
                    if selection_parameters["document_close_user"]:
                        q &= Q(document_close_user__contains=selection_parameters["document_close_user"])
                    if selection_parameters["session"]:
                        q &= Q(session__exact=selection_parameters["session"])
                    if selection_parameters["shop"]:
                        q &= Q(shop__exact=selection_parameters["shop"])
                    if selection_parameters["workplace"]:
                        q &= Q(workplace__exact=selection_parameters["workplace"])
                    if selection_parameters["doc_number"]:
                        q &= Q(doc_number__exact=selection_parameters["doc_number"])
                total = Transaction.objects.filter(q).count()
                if data["count"] > total:
                    data["count"] = total
                trans = Transaction.objects.filter(q).order_by('-'+selection_parameters["sort"]).all()[data["start"]:data["start"]+data["count"]]
                resp_cards = []
                for tran in trans:
                    resp_cards.append(
                        {
                            "type": tran.return_type(),
                            "date": tran.date.strftime('%Y-%m-%d / %H:%M'),
                            "card": tran.card.code,
                            "sum": tran.sum,
                            "bonus_before": tran.bonus_before,
                            "bonus_add": tran.bonus_add,
                            "bonus_reduce": tran.bonus_reduce,
                            "workplace": tran.workplace,
                            "doc_number": tran.doc_number,
                            "session": tran.session,
                            "doc_external_id": tran.doc_external_id,
                            "doc_close_user": tran.doc_close_user,
                            "shop": tran.shop
                        }
                    )

                response = {"result": "ok", "data": resp_cards, "total": total}
                return HttpResponse(json.dumps(response), content_type="application/json")


# REST API VIEWS
@csrf_exempt
def rest_transactions_list(request):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)

        trans = Transaction.objects.filter(org_id__exact=user.org.pk).order_by('-date')[:100]

        serializer_context = {
            'request': Request(request),
        }

        serializer = TransactionSerializer(trans, many=True, context=serializer_context)

        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def rest_trans_by_card(request, card_code):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        try:
            card = Card.objects.get(code__exact=card_code, org_id__exact=user.org.pk)
        except Exception as e:
            response['error'] = str(e)
            return JsonResponse(response, status=400)

        trans = Transaction.objects.filter(org_id__exact=user.org.pk, card_id__exact=card.pk)[:100]

        serializer_context = {
            'request': Request(request),
        }

        serializer = TransactionSerializer(trans, many=True, context=serializer_context)

        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = json.loads(request.body.decode())
        count = 20
        if 'count' in data:
            count = int(data['count'])

        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        try:
            card = Card.objects.get(code__exact=card_code, org_id__exact=user.org.pk)
        except Exception as e:
            response['error'] = str(e)
            return JsonResponse(response, status=400)

        trans = Transaction.objects.filter(org_id__exact=user.org.pk, card_id__exact=card.pk).order_by('-date')[:count]

        serializer_context = {
            'request': Request(request),
        }

        serializer = TransactionSerializer(trans, many=True, context=serializer_context)

        return JsonResponse(serializer.data, safe=False)


def rest_discount_trans_by_card(request, card_code):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        try:
            card = Card.objects.get(code__exact=card_code, org_id__exact=user.org.pk)
        except Exception as e:
            response['error'] = str(e)
            return JsonResponse(response, status=400)

        trans = Transaction.objects.filter(org_id__exact=user.org.pk,
                                           card_id__exact=card.pk,
                                           type__exact=Operations.discount_recount)

        serializer_context = {
            'request': Request(request),
        }

        serializer = TransactionSerializer(trans, many=True, context=serializer_context)

        return JsonResponse(serializer.data, safe=False)
