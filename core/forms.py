from django import forms
from .models import DiscountPlan


class SettingsForm(forms.Form):
    #algorithm = forms.ChoiceField(DiscountPlan.algorithm_choices, label='Режим дисконтной системы')

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control '


class BonusForm(SettingsForm):
    round_choices = (
        ('math', 'Математическое округление'),
        ('up','В большую сторону'),
        ('down','В меньшую сторону'),
        ('None', 'Без округления')
    )
    zeroing_choices = (
        (0, 'Не обнулять'),
        (1, 'Через месяц'),
        (3, 'Через квартал'),
        (6, 'Через полгода'),
        (12, 'Через год')
    )
    min_transaction = forms.FloatField(label='Минимальный порог оплаты для зачисления Бонуса',
                                       min_value=0, initial=100)
    max_bonus_percentage = forms.FloatField(label='Сколько процентов от суммы покупки можно оплатить бонусами',
                                       min_value=0, initial=100, max_value=100)
    bonus_cost = forms.FloatField(label='Стоимость 1 бонуса', min_value=1, initial=100)
    round = forms.ChoiceField(round_choices, label='Округление суммы покупки для начисления бонусов')
    assume_delta = forms.FloatField(label='Задержка перед начислением бонуса, часы', min_value=0, initial=0)
    zeroing_delta = forms.IntegerField(min_value=0, initial=0,
                                       label='Обнуление бонусов неактивных карт через выбранное количество дней. "0" - не обнулять')


class DiscountForm(SettingsForm):
    zeroing_choices = (
        (0, 'Не обнулять'),
        (1, 'Через месяц'),
        (3, 'Через квартал'),
        (6, 'Через полгода'),
        (12, 'Через год')
    )

    rules = forms.CharField(widget=forms.TextInput, label='Правила начисления скидок')


class ComboForm(SettingsForm):
    round_choices = (
        ('up', 'В большую сторону'),
        ('down', 'В меньшую сторону'),
        ('math', 'Математическое округление'),
        ('None', 'Без округления')
    )

    zeroing_choices = (
        (0, 'Не обнулять'),
        (1, 'Через месяц'),
        (3, 'Через квартал'),
        (6, 'Через полгода'),
        (12, 'Через год')
    )
    rules = forms.CharField(widget=forms.TextInput, label='Правила начисления скидок')

    bonus_cost = forms.FloatField(label='Стоимость 1 бонуса', min_value=1, initial=100)
    min_transaction = forms.FloatField(label='Минимальный порог оплаты для зачисления Бонуса',
                                       min_value=0, initial=100)
    max_bonus_percentage = forms.FloatField(label='Сколько процентов от суммы покупки можно оплатить бонусами',
                                            min_value=0, initial=100, max_value=100)
    round = forms.ChoiceField(round_choices, label='Округление суммы покупки для начисления бонусов')
    assume_delta = forms.FloatField(label='Задержка перед начислением бонуса, часы', min_value=0, initial=0)
    zeroing_delta = forms.IntegerField(min_value=0, initial=0,
                                       label='Обнуление бонусов неактивных карт через выбранное количество дней. "0" - не обнулять')