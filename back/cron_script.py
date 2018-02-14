
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
    from cards.models import Card, Bonus
    from transactions.models import Transaction
    from datetime import datetime

    # tasks = Task.objects.all()
    # for task in tasks:
    #     try:
    #         test = Card.objects.get(id__exact=task.card.pk)
    #     except:
    #         task.delete()
    #         continue
    #
    #     if test.deleted == 'y':
    #         task.delete()
    #         continue
    #
    #     if task.execution_date <= datetime.now():
    #         _handler = __import__('core.lib.%s' % task.operation, globals(), locals(),
    #                                                  ['count'], 0)
    #         card = _handler.count(task.data, task.card, task.d_plan, task.transaction)
    #         card.save()
    #         task.delete()

    for bonus in Bonus.objects.filter(enabled__exact=False):
        if bonus.active_from.date() >= datetime.now().date():
            bonus.enabled = True
            try:
                task = Task.objects.get(id__exact=bonus.task_id)
                task.delete()
            except:
                pass
            bonus.save()
