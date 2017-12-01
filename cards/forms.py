from django import forms
from .models import Card


class CardForm(forms.Form):
    code = forms.CharField(label='КОД*')
    holder_name = forms.CharField(label='ФИО Владельца', required=False)
    holder_phone = forms.CharField(label='Телефон', required=False)
    accumulation = forms.FloatField(label='Накопления*',  min_value=0, disabled=False, initial=0)
    bonus = forms.FloatField(label='Бонусы*', min_value=0, disabled=False, initial=0)
    discount = forms.FloatField(label='Скидка*', min_value=0, disabled=False, initial=0)
    type = forms.ChoiceField(choices=Card.type_choices, label='Тип карты*')
    reg_date = forms.DateField(disabled=True, required=False, label='Дата регистрации')
    changes_date = forms.DateField(disabled=True, required=False, label='Дата последних изменений')
    last_transaction_date = forms.DateField(disabled=True, required=False, label='Дата последней транзакции')


    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'


class MassCardForm(forms.Form):

    doubles_choices = (
        ('append', 'Перезаписать, сохранив ФИО'),
        ('rewrite', 'Перезаписать на новую'),
        ('ignore', 'Оставить существующую карту без изменений')
    )

    code_start = forms.IntegerField(label='Начальный КОД', min_value=0, required=True)
    code_end = forms.IntegerField(label='Конечный КОД', min_value=0, required=True)
    code_length = forms.IntegerField(label='Длина КОДА', min_value=0, required=True)
    accumulation = forms.FloatField(label='Накопления',  min_value=0, disabled=False, initial=0, required=True)
    bonus = forms.FloatField(label='Бонусы', min_value=0, disabled=False, initial=0, required=True)
    discount = forms.FloatField(label='Скидка', min_value=0, disabled=False, initial=0, required=True)
    type = forms.ChoiceField(choices=Card.type_choices, label='Тип карты', required=True)
    doubles = forms.ChoiceField(choices=doubles_choices, label='Если карта с таким кодом существует', required=True)

    def __init__(self, *args, **kwargs):
        super(MassCardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'
