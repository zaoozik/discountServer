import json
from datetime import datetime, timedelta
from transactions.models import Transaction
from core.models import Operations
from cards.models import Bonus
#
# bonus_cost = None
# min_transaction = None
# zeroing_delta = None


def custom_round(value, rounding):
    if value % 1 == 0:
        return value
    if rounding == 'None':
        return value
    if rounding == 'up':
        return value // 1 + 1
    if rounding == 'down':
        return value // 1
    if rounding == 'math':
        return round(value)
    return None


def count(value, card, d_plan, transaction):
    try:
        parameters = json.loads(d_plan.parameters)
    except:
        return None
    if type(parameters) is not dict:
        return None
    value = float(value)

    if 'bonus_mechanism' in parameters:
        bonus_mechanism = parameters['bonus_mechanism']
    else:
        return None

    if bonus_mechanism == 'bonus_cost':
        if 'bonus_cost' in parameters:
            bonus_cost = float(parameters['bonus_cost'])
        else:
            return None

    if bonus_mechanism == 'bonus_percent':
        if 'bonus_percent' in parameters:
            bonus_percent = float(parameters['bonus_percent'])
        else:
            return None

    if 'min_transaction' in parameters:
        min_transaction = float(parameters['min_transaction'])
    else:
        return None

    if 'bonus_lifetime' in parameters:
        bonus_lifetime = float(parameters['bonus_lifetime'])
    else:
        return None

    if 'round' in parameters:
        rounding = parameters['round']
    else:
        return None

    if abs(value) < min_transaction:
        return card
    if value <0:
        op_type = Operations.bonus_refund
    else:
        op_type = Operations.bonus_add
    trans = Transaction(
        org=card.org,
        card=card,
        date=datetime.now(),
        type=op_type,
        bonus_before=card.get_total_bonus(),
        doc_number=transaction.doc_number,
        session=transaction.session,
        sum=transaction.sum,
        shop=transaction.shop,
        workplace=transaction.workplace
    )

    bonus = Bonus()
    bonus.active_from = datetime.now()
    bonus.card = card
    if bonus_mechanism == 'bonus_cost':
        bonus.value = custom_round((value / bonus_cost), rounding)
    elif bonus_mechanism == 'bonus_percent':
        bonus.value = custom_round((value * bonus_percent / 100), rounding)

    bonus.active_to = bonus.active_from + timedelta(days=bonus_lifetime)

    trans.bonus_add = bonus.value
    trans.save()
    bonus.save()

    return card


def rem_bonus(card, in_value):
    value = float(in_value)
    bonuses = card.get_bonuses_lifo()
    for bonus in bonuses:
        if bonus.value < value:
            value -= bonus.value
            bonus.delete()
            continue
        elif bonus.value == value:
            bonus.delete()
            break
        else:
            bonus.value -= value
            bonus.save()
            break


def refund_bonus(card, refund_bonus):
    bonuses = card.get_bonuses()
    for bonus in bonuses:
        if bonus.value < value:
            value -= bonus.value
            bonus.delete()
            continue
        elif bonus.value == value:
            bonus.delete()
            break
        else:
            bonus.value -= value
            bonus.save()
            break