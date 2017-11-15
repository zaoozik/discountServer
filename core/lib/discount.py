import json
from collections import OrderedDict


def count(value, card, json_str_parameters):
    try:
        parameters = json.loads(json_str_parameters)
    except:
        return None
    if type(parameters) is not dict:
        return None

    value = float(value)

    if 'rules' in parameters:
        rules = eval(parameters['rules'])
    else:
        return None

    if 'base_discount' in parameters:
        base_discount = float(parameters['base_discount'])
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
    card.accumulation += value
    next_discount = None

    rules_iter = iter(sorted(rules.items(), key=lambda item: item[0]))
    for rule in rules_iter:
        if rule[0] == card.discount:
            next_discount = rules_iter.__next__()
            if next_discount[1] <= card.accumulation:
                card.discount = next_discount[0]
            else:
                break;
    if next_discount[1] <= card.accumulation:
        card.discount = next_discount[0]

    return card

