import json
from django.shortcuts import render
from .models import Transaction
from django.contrib.auth.decorators import login_required
from users.models import UserCustom
from cards.models import Card
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.template import loader
from django.db.models import Q


# Create your views here.
@login_required
def listTrans(request):
    if request.method=="GET":
        response = {}
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
                resp_cards=[]
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
