from django.utils.translation import ugettext_lazy as _
from django import forms

class NetpayForm(forms.Form):
    money = forms.IntegerField(
        label='Сумма в рублях',
        )
