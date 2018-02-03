from django import forms
from .models import Transaction


class ControlsForm(forms.Form):
    date_from = forms.DateField(label='', )
    date_to = forms.DateField(label='')

    def __init__(self, *args, **kwargs):
        super(ControlsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'
            self.fields[field].widget.attrs['style'] = 'margin-right: 15px;'