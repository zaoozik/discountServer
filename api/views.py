from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card
from users.models import UserCustom
from transactions.models import Transaction
from core.models import DiscountPlan
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.utils.decorators import method_decorator


# Create your views here.
@csrf_exempt
def apiGetCardBonus(request, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data):
            try:
                cuser = UserCustom.objects.get(frontol_access_key__exact=data['key'])
            except:
                cuser = None
            if cuser is not None:
                if cuser.user.is_active:
                    try:
                        card = Card.objects.get(code=card_code, org=cuser.org.pk, deleted='n')
                        return HttpResponse(card.bonus, status='200')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')


@csrf_exempt
def apiGetCardDiscount(request, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data):
            try:
                cuser = UserCustom.objects.get(frontol_access_key__exact=data['key'])
            except:
                cuser = None
            if cuser is not None:
                if cuser.user.is_active:
                    try:
                        card = Card.objects.get(code=card_code, org=cuser.org.pk, deleted='n')
                        return HttpResponse(card.discount, status='200')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')



@csrf_exempt
def apiAddAccumToCard(request, card_code, salt):
    t_type = 'assume'
    if request.method == 'POST':
        data = request.POST
        if ('key' in data):
            try:
                cuser = UserCustom.objects.get(frontol_access_key__exact=data['key'])
            except:
                cuser = None
            if cuser is not None:
                if cuser.user.is_active:
                    try:
                        if 'value' in data:
                            trans = Transaction().create(data)
                            trans.date = datetime.now()
                            card = Card.objects.get(code=card_code, org=cuser.org.pk)

                            trans.bonus_before = card.bonus

                            d_plan = DiscountPlan.objects.get(org_id__exact=cuser.org.pk)
                            algorithm = d_plan.algorithm

                            #подключаем обработчик начислений
                            _discounter = __import__('core.lib.%s' % algorithm, globals(), locals(),
                                                 ['count'], 0)

                            card = _discounter.count(data['value'], card, d_plan.parameters)
                            card.save()
                            # пишем статистику
                            trans.org = cuser.org
                            trans.card = card
                            trans.sum = float(data['value'])
                            trans.bonus_reduce = 0
                            trans.bonus_add = card.bonus - trans.bonus_before
                            trans.type = t_type
                            trans.save()

                            return HttpResponse(data['value'])
                        else:
                            return HttpResponse(status='404')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')


@csrf_exempt
def apiRemCardBonus(request, card_code, salt):
    t_type= 'reduce'
    if request.method == 'POST':
        data = request.POST
        if ('key' in data):
            try:
                cuser = UserCustom.objects.get(frontol_access_key__exact=data['key'])
            except:
                cuser = None
            if cuser is not None:
                if cuser.user.is_active:
                    try:
                        if 'value' in data:
                            trans = Transaction().create(data)
                            trans.date = datetime.now()

                            card = Card.objects.get(code=card_code, org=cuser.org.pk)

                            trans.bonus_before = card.bonus

                            # пишем статистику
                            trans.org = cuser.org
                            trans.card = card
                            trans.sum = 0
                            trans.bonus_reduce = float(data['value'])
                            trans.type = t_type
                            trans.save()

                            card.bonus -= float(data['value'])
                            card.save()
                            return HttpResponse(data['value'])
                        else:
                            return HttpResponse(status='404')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')


@csrf_exempt
def apiGetDiscountPlan(request, salt):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data):
            try:
                cuser = UserCustom.objects.get(frontol_access_key__exact=data['key'])
            except:
                cuser = None
            if cuser is not None:
                if cuser.user.is_active:
                    try:
                        d_plan = DiscountPlan.objects.get(org_id__exact=cuser.org.pk)
                        algorithm = d_plan.algorithm
                        return HttpResponse(algorithm)

                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')
    return HttpResponse(status='503')