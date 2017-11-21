import json
from transactions.models import Transaction
from core.models import Operations
from datetime import datetime


class DiscountParameters:
    def __init__(self, **kwargs):
        self.len = 0
        self.current = 0
        self.first = 0
        self.last = 0
        self.body = []

    def load(self, params):
        if type(params) == dict:
            self.body = sorted(params.items(), key=lambda item: item[0])
            self.len = len(self.body)
            if self.len > 0:
                self.current = 0
                self.first = 0
                self.last = self.len-1
            else:
                self.current = None
                self.first = None
                self.last = None
        return self

    def get_current(self):
        return self.body[self.current]

    def next(self):
        current = self.current+1
        if current > self.last:
            return None
        else:
            self.current = current
        return self.body[self.current]

    def previous(self):
        current = self.current -1
        if current < self.first:
            return  None
        else:
            self.current = current
        return self.body[self.current]


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

    rules = DiscountParameters().load(rules)
    next_discount = None
    while rules.current<=rules.last:
        if rules.get_current()[0] == card.discount:
            next_discount = rules.next()
            if next_discount is None:
                return card
            if next_discount[1] <= card.accumulation:
                card.discount = next_discount[0]

                trans = Transaction(
                    org=card.org,
                    card=card,
                    date=datetime.now(),
                    type=Operations.discount_recount,
                    bonus_add=card.discount,
                )
                trans.save()

            else:
                return card
        else:
            rules.next()



    return card

