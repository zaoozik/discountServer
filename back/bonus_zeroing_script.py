
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

    from cards.models import Card
    from django.db.models import Q
    from cards.models import Bonus
    from datetime import datetime, timedelta

    for bonus in Bonus.objects.all():
        if bonus.active_to.date() > datetime.now().date():
            print("Removing bonus " + bonus.card.org + " " + bonus.card.code)
            bonus.delete()

    # for d_plan in DiscountPlan.objects.filter(algorithm__exact='bonus'):
    #     params = d_plan.get_params()
    #     if params:
    #         if 'zeroing_delta' in params:
    #             delta = int(params['zeroing_delta'])
    #             if  delta == 0:
    #                 continue
    #             else:
    #                 print("ORG: " + d_plan.org.name)
    #                 filter = Q(org_id__exact=d_plan.org.pk)
    #                 a = datetime.now().date()- timedelta(hours=24*delta)
    #                 cards = Card.objects.filter(filter)
    #                 for card in cards:
    #                     print("card: " + card.code)
    #                     if card.last_transaction_date <= a:
    #                         card.bonus = 0
    #                         card.save()
