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
    from orgs.models import Org
    import xlrd
    import re
    from datetime import datetime

    rb = xlrd.open_workbook('sport_import.xlsx')
    sheet = rb.sheet_by_index(0)

    org = Org.objects.get(id__exact=3)
    for nrow in range(sheet.nrows):
        card = Card()
        if nrow == 0:
            continue
        row = sheet.row_values(nrow)
        name = row[0]
        name = re.sub(r'[0-9]+', '', name)
        name = name.strip()
        name = name.title()

        card.holder_name = name

        code = row[1]
        card.code = str(code)

        reg_date = row[2]
        try:
            card.reg_date = datetime.strptime(reg_date, '%d.%m.%Y')
        except:
            card.reg_date = None

        sex = row[3]
        if sex == 'муж':
            card.sex = 'm'
        elif sex == 'жен':
            card.sex = 'f'
        else:
            card.sex = 'm'


        fav_date = row[4]
        try:
            card.fav_date = datetime.strptime(fav_date, '%d.%m.%Y')
        except:
            card.fav_date = None

        accum = row[7]
        card.accumulation = float(accum)

        phone = row[9]
        try:
            phone = str(int(phone))
        except:
            phone = str(phone)
        card.holder_phone = phone

        card.last_transaction_date = datetime.now().date()
        card.changes_date = datetime.now().date()

        card.org = org
        card.save()

        # try:
        #     card.save()
        # except django.db.utils.IntegrityError as er:
        #     continue

        pass



