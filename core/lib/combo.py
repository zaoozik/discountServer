from .bonus import count as bonus_count
from .discount import count as discount_count

def count (value, card, d_plan, transaction):
    this_card = bonus_count(value, card, d_plan, transaction)
    this_card = discount_count(value, this_card, d_plan, transaction)