from django import forms
from .models import DiscountPlan


class SettingsForm(forms.Form):
    algorithm = forms.ChoiceField(DiscountPlan.algorithm_choices, label='Режим дисконтной системы')

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control '


class BonusForm(SettingsForm):
    round_choices = (
        ('up','В большую сторону'),
        ('down','В меньшую сторону'),
        ('math', 'Математическое округление'),
        ('None', 'Без округления')
    )
    zeroing_choices = (
        (0, 'Не обнулять'),
        (1, 'Каждый месяц'),
        (3, 'Каждый квартал'),
        (6, 'Каждые полгода'),
        (12, 'Каждый год')
    )
    min_transaction = forms.FloatField(label='Минимальный порог оплаты для зачисления Бонуса',
                                       min_value=0, initial=100)
    bonus_cost = forms.FloatField(label='Стоимость 1 бонуса', min_value=1, initial=100)
    round = forms.ChoiceField(round_choices, label='Режим округления накоплений для зачисления бонусов')
    assume_delta = forms.FloatField(label='Задержка перед начислением бонуса, часы', min_value=0, initial=0)
    zeroing_delta = forms.ChoiceField(zeroing_choices, label='Обнуление бонусов')


class DiscountForm(SettingsForm):
    zeroing_choices = (
        (0, 'Не обнулять'),
        (1, 'Каждый месяц'),
        (3, 'Каждый квартал'),
        (6, 'Каждые полгода'),
        (12, 'Каждый год')
    )

    rules = forms.CharField(widget=forms.TextInput, label='Правила начисления скидок')
    base_discount = forms.FloatField(label='Базовая скидка', min_value=0, initial=0)
    assume_delta = forms.FloatField(label='Задержка перед начислением скидки, часы', min_value=0, initial=0)
    zeroing_delta = forms.ChoiceField(zeroing_choices, label='Обнуление скидки')
