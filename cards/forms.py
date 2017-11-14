from django import forms
from .models import Card


class CardForm(forms.Form):
    code = forms.CharField(label='КОД')
    holder_name = forms.CharField(label='ФИО Владельца')
    accumulation = forms.FloatField(label='Накопления', disabled=True, initial=0)
    bonus = forms.FloatField(label='Бонусы', disabled=True, initial=0)
    discount = forms.FloatField(label='Скидка', disabled=True, initial=0)


    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


