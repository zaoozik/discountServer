from django import forms


class CashBoxForm(forms.Form):
    name = forms.CharField(label='Наименование*')
    serial_number = forms.IntegerField(min_value=0, label='Номер кассы*')
    address = forms.CharField(label='Адрес кассы*')
    frontol_version = forms.CharField(label='Версия Frontol*')

    def __init__(self, *args, **kwargs):
        super(CashBoxForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control form-control-sm'