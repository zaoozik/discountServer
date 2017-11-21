from django import forms
from .models import Card


class CardForm(forms.Form):
    code = forms.CharField(label='КОД')
    holder_name = forms.CharField(label='ФИО Владельца')
    accumulation = forms.FloatField(label='Накопления',  min_value=0, disabled=False, initial=0)
    bonus = forms.FloatField(label='Бонусы', min_value=0, disabled=False, initial=0)
    discount = forms.FloatField(label='Скидка', min_value=0, disabled=False, initial=0)
    type = forms.ChoiceField(choices=Card.type_choices, label='Тип карты')
    reg_date = forms.DateField(disabled=True, required=False, label='Дата регистрации')
    changes_date = forms.DateField(disabled=True, required=False, label='Дата последних изменений')
    last_transaction_date = forms.DateField(disabled=True, required=False, label='Дата последней транзакции')


    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'


