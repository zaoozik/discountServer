import json
from datetime import datetime
from transactions.models import Transaction
from core.models import Operations
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


def count (value, card, d_plan, transaction):
    try:
        parameters = json.loads(d_plan.parameters)
    except:
        return None
    if type(parameters) is not dict:
        return None

    value = float(value)

    if 'bonus_cost' in parameters:
        bonus_cost = float(parameters['bonus_cost'])
    else:
        return None

    if 'min_transaction' in parameters:
        min_transaction = float(parameters['min_transaction'])
    else:
        return None

    if 'zeroing_delta' in parameters:
        zeroing_delta = float(parameters['zeroing_delta'])
    else:
        return None

    if 'round' in parameters:
        rounding = parameters['round']
    else:
        return None

    if value < min_transaction:
        return card

    trans = Transaction(
        org=card.org,
        card=card,
        date=datetime.now(),
        type=Operations.bonus_add,
        bonus_before=card.bonus,
        doc_number=transaction.doc_number,
        session=transaction.session,
        sum=transaction.sum,
        shop=transaction.shop,
        workplace=transaction.workplace
    )

    card.bonus += custom_round((value / bonus_cost), rounding)
    trans.bonus_add = card.bonus - trans.bonus_before
    trans.save()

    return card
