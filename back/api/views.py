from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card
from users.models import UserCustom
from orgs.models import CashBox
from transactions.models import Transaction
from core.models import DiscountPlan, Operations
from queues.models import Task
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from django.utils.decorators import method_decorator
from core.lib.bonus import rem_bonus
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse


def identify_task_operation(card, d_plan):
    if d_plan.is_bonus():
        if card.is_bonus():
            return 'bonus'
        elif card.is_combo():
            return 'bonus'
        elif card.is_discount():
            return None
    elif d_plan.is_discount():
        if card.is_bonus():
            return None
        elif card.is_combo():
            return 'discount'
        elif card.is_discount():
            return 'discount'
    elif d_plan.is_combo():
        if card.is_bonus():
            return 'bonus'
        elif card.is_combo():
            return 'combo'
        elif card.is_discount():
            return 'discount'




def check_license(key, ses_key):
    try:
        box = CashBox.get_by_key(key)
        if box:
            if box.session_key is None:
                return False
            if box.session_key == ses_key:
                return box
            else:
                return False
        else:
            return False
    except ObjectDoesNotExist as e:
        return False



@csrf_exempt
def apiOpenSession(request, salt):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data) and ('session_key' in data):
            box = CashBox.get_by_key(data['key'])
            if box:
                if not box.online:
                    box.session_key = data['session_key']
                    box.set_online()
                    return HttpResponse("1", status=200)
                return HttpResponse("1", status=503)
    return HttpResponse(status=404)


@csrf_exempt
def apiCloseSession(request, salt):
    if request.method == 'POST':
        data = request.POST
        if 'key' in data:
            box = CashBox.get_by_key(data['key'])
            if box:
                box.session_key = None
                box.set_offline()
                return HttpResponse("1", status=200)
    return HttpResponse(status=404)


# Create your views here.
@csrf_exempt
def apiGetCard(request, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data) and ('session_key' in data):
            box = check_license(data['key'], data['session_key'])
            if box:
                try:
                    org = box.co_unit.org
                except:
                    return HttpResponse(status=403)
                    org = None
            else:
                return HttpResponse(status=403)
            if org is not None:
                if org.is_active:
                    try:
                        card = Card.objects.get(code=card_code, org=org.pk, deleted='n')
                        d_plan = DiscountPlan.objects.get(org=org.pk)
                        # Логика взаимодействия режима дисконтной системы и типов карт
                        # В комбинированном режиме работают дисконтные, бонусные и комбинированные карты.
                        # В режиме"Бонусы" работают бонусные и комбинированные карты.
                        # В режиме "Накопительная скидка" работают дисконтные карты и комбинированные
                        #

                        if card.is_bonus():
                            if not d_plan.is_discount():
                                return HttpResponse(('%s#%s#%s') % (card.get_total_bonus(), 0, card.accumulation), status='200')
                            else:
                                return HttpResponse(('%s#%s#%s') % (0, 0, card.accumulation), status='200')
                        if card.is_discount():
                            if not d_plan.is_bonus():
                                return HttpResponse(('%s#%s#%s') % (0, card.discount, card.accumulation), status='200')
                            else:
                                return HttpResponse(('%s#%s#%s') % (0, 0, card.accumulation), status='200')
                        if card.is_combo():
                            if d_plan.is_combo():
                                return HttpResponse(('%s#%s#%s') % (card.get_total_bonus(), card.discount, card.accumulation), status='200')
                            elif d_plan.is_bonus():
                                return HttpResponse(('%s#%s#%s') % (card.get_total_bonus(), 0, card.accumulation), status='200')
                            elif d_plan.is_discount():
                                return HttpResponse(('%s#%s#%s') % (0, card.discount, card.accumulation), status='200')
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
    t_type = Operations.sell
    if request.method == 'POST':
        data = request.POST
        if ('key' in data) and ('session_key' in data):
            box = check_license(data['key'], data['session_key'])
            if box:
                try:
                    org = box.co_unit.org
                except:
                    return HttpResponse(status=403)
                    org = None
            else:
                return HttpResponse(status=403)
            if org is not None:
                if org.is_active:
                    try:
                        if 'value' in data:
                            value = float(data['value'])
                            trans = Transaction().create(data)
                            trans.date = datetime.now()
                            card = Card.objects.get(code=card_code, org=org.pk)

                            trans.bonus_before = card.get_total_bonus()
                            trans.org = org
                            trans.card = card
                            trans.sum = float(data['value'])
                            trans.bonus_reduce = 0
                            trans.type = t_type
                            try:
                                trans.base_doc_date = parse(data['base_doc_date'])
                            except:
                                trans.base_doc_date = None

                            d_plan = DiscountPlan.objects.get(org_id__exact=org.pk)

                            algorithm = d_plan.algorithm
                            card.accumulation += float(data['value'])
                            card.last_transaction_date = datetime.now().date()
                            card.save()

                            if value <0:
                                t_type = Operations.refund
                                trans.type = t_type
                                _handler = __import__('core.lib.%s' % identify_task_operation(card, d_plan),
                                                      globals(), locals(),['count'], 0)
                                card = _handler.count(value, card, d_plan, trans)
                                card.save()


                            trans.save()

                            if value >0:
                                try: # Добавляем задание
                                    # task = Task(queue_date=datetime.now(),
                                    #             execution_date= datetime.now().date() + relativedelta(days=d_plan.time_delay),
                                    #             data=data['value'],
                                    #             card=card,
                                    #             operation=identify_task_operation(card, d_plan),
                                    #             d_plan=d_plan,
                                    #             transaction=trans,
                                    #             org=card.org)
                                    # task.save()

                                    _handler = __import__('core.lib.%s' % identify_task_operation(card, d_plan),
                                                          globals(), locals(), ['count'], 0)
                                    card = _handler.count(value, card, d_plan, trans)
                                    card.save()

                                except:
                                    pass

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
def apiToCardFromService(request):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data) and ('vtikeeper' in data):
            box = CashBox.get_by_key(data['key'])
            if box:
                try:
                    org = box.co_unit.org
                except:
                    org = None
            if org is not None:
                if org.is_active:
                    try:
                        if 'type' in data:
                            if data['type'] == 'add':
                                t_type = Operations.sell
                                if 'value' in data and 'card' in data:
                                    trans = Transaction().create(data)
                                    trans.date = datetime.strptime(data['datetime'], "%d.%m.%Y %H:%M:%S")
                                    card = Card.objects.get(code=data['card'], org=org.pk)

                                    trans.bonus_before = card.get_total_bonus()

                                    d_plan = DiscountPlan.objects.get(org_id__exact=org.pk)
                                    algorithm = d_plan.algorithm
                                    card.accumulation += float(data['value'])
                                    card.last_transaction_date = datetime.now().date()
                                    card.save()

                                    # пишем статистику
                                    trans.org = org
                                    trans.card = card
                                    trans.sum = float(data['value'])
                                    trans.bonus_reduce = 0
                                    trans.type = t_type

                                    try:
                                        trans.base_doc_date = parse(data['base_doc_date'])
                                    except:
                                        trans.base_doc_date = None

                                    trans.save()

                                    try: # Добавляем задание
                                        task = Task(queue_date=datetime.now(),
                                                    execution_date= trans.date + relativedelta(days=d_plan.time_delay),
                                                    data=data['value'],
                                                    card=card,
                                                    operation=identify_task_operation(card, d_plan),
                                                    d_plan=d_plan,
                                                    transaction=trans,
                                                    org=card.org)
                                        task.save()
                                    except:
                                        pass


                                    return HttpResponse(data['value'])
                                else:
                                    return HttpResponse(status='404')
                            if data['type'] == 'rem':
                                t_type = Operations.bonus_reduce
                                if 'value' in data and 'card' in data:
                                    trans = Transaction().create(data)
                                    trans.date = datetime.strptime(data['datetime'], "%d.%m.%Y %H:%M:%S")
                                    card = Card.objects.get(code=data['card'], org=org.pk)

                                    trans.bonus_before = card.get_total_bonus()

                                    # пишем статистику
                                    trans.org = org
                                    trans.card = card
                                    trans.sum = 0
                                    trans.bonus_reduce = float(data['value'])
                                    trans.type = t_type
                                    trans.save()

                                    value = float(data['value'])
                                    rem_bonus(card, value)

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
    t_type = Operations.bonus_reduce
    if request.method == 'POST':
        data = request.POST
        if ('key' in data) and ('session_key' in data):
            box = check_license(data['key'], data['session_key'])
            if box:
                try:
                    org = box.co_unit.org
                except:
                    return HttpResponse(status=403)
                    org = None
            else:
                return HttpResponse(status=403)
            if org is not None:
                if org.is_active:
                    try:
                        if 'value' in data:
                            trans = Transaction().create(data)
                            trans.date = datetime.now()

                            card = Card.objects.get(code=card_code, org=org.pk)

                            trans.bonus_before = card.get_total_bonus()

                            # пишем статистику
                            trans.org = org
                            trans.card = card
                            trans.sum = 0
                            trans.bonus_reduce = float(data['value'])
                            trans.type = t_type
                            trans.save()

                            value = float(data['value'])
                            rem_bonus(card, value)

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
def apiGetParams(request, salt):
    if request.method == 'POST':
        data = request.POST
        if ('key' in data) and ('session_key' in data):
            box = check_license(data['key'], data['session_key'])
            if box:
                try:
                    org = box.co_unit.org
                except:
                    return HttpResponse(status=403)
                    org = None
            else:
                return HttpResponse(status=403)
            if org is not None:
                if org.is_active:
                    try:
                        d_plan = DiscountPlan.objects.get(org_id__exact=org.pk)
                        params = d_plan.get_params()
                        if params:
                            response = ("%s;" % params['max_bonus_percentage'])
                        else:
                            response = 0

                        return HttpResponse(response)

                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')
    return HttpResponse(status='503')