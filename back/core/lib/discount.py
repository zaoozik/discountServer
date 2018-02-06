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
        if type(params) == list:
            params.append([0, 0])
            params = [[float(item[0]), float(item[1])] for item in params]
            self.body = sorted(params, key=lambda item: float(item[0]))
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

    def get_previous(self):
        current = self.current - 1
        if current < self.first:
            return None
        return self.body[current]

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


def count(value, card,  d_plan, transaction):
    # try:
    #     parameters = json.loads(d_plan.parameters)
    # except:
    #     return None
    # if type(parameters) is not dict:
    #     return None

    try:
        rules = json.loads(d_plan.rules)
    except:
        return None
    if type(rules) is not list:
        return None

    value = float(value)


    rules = DiscountParameters().load(rules)
    next_discount = None
    if value >= 0:
        while rules.current <= rules.last:
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
                        doc_number=transaction.doc_number,
                        session=transaction.session,
                        sum=transaction.sum,
                        shop=transaction.shop,
                        workplace=transaction.workplace
                    )
                    trans.save()

                else:
                    return card
            else:
                rules.next()

    if value < 0:
        rules.current = rules.last
        while rules.current >= rules.first:
            if rules.get_current()[0] == card.discount:
                next_discount = rules.get_previous()
                if next_discount is None:
                    return card
                if rules.get_current()[1] > card.accumulation:
                    card.discount = next_discount[0]

                    trans = Transaction(
                        org=card.org,
                        card=card,
                        date=datetime.now(),
                        type=Operations.discount_recount,
                        bonus_add=card.discount,
                        doc_number=transaction.doc_number,
                        session=transaction.session,
                        sum=transaction.sum,
                        shop=transaction.shop,
                        workplace=transaction.workplace
                    )
                    trans.save()

                else:
                    return card
            else:
                rules.previous()

    return card

