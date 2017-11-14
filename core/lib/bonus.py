import json
from datetime import datetime
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


def count (value, json_str_parameters):
    try:
        parameters = json.loads(json_str_parameters)
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

    if 'assume_delta' in parameters:
        assume_delta = float(parameters['zeroing_delta'])
    else:
        return None

    if 'round' in parameters:
        rounding = parameters['round']
    else:
        return None

    if float(value) < min_transaction:
        return 0

    bonus = custom_round((value / bonus_cost), rounding)

    return bonus