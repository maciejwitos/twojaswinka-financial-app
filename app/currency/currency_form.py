from app.user.user_forms import *


class AddCurrencyForm(forms.Form):
    name = forms.CharField(max_length=16)
    in_pln = forms.FloatField()
