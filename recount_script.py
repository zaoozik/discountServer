
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "discountServer.settings")
    try:
        import django
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        raise

    django.setup()

    from queues.models import Task
    from cards.models import Card
    from core.models import DiscountPlan
    from transactions.models import Transaction
    from datetime import datetime

    cards = Card.objects.filter(org_id__exact=3)
    d_plan = DiscountPlan.objects.get(org_id__exact=3)
    for card in cards:
        print(card.code)

        _handler = __import__('core.lib.%s' % d_plan.algorithm, globals(), locals(),
                                                     ['count'], 0)
        card = _handler.count(0, card, d_plan, Transaction())
        card.save()
        print('New discount = %s.' % card.discount)

