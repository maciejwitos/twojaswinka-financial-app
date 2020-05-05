from app.user.user_forms import *


class AddAccountForm(forms.Form):
    name = forms.CharField(max_length=24, label='Nazwa', widget=(forms.TextInput({'class': 'form-control', 'placeholder': 'np. ROR Beata'})))
    bank = forms.CharField(max_length=24, label='Bank', widget=(forms.TextInput({'class': 'form-control', 'placeholder': 'np. PKO'})))
    balance = forms.FloatField(label='Saldo', widget=(forms.NumberInput({'class': 'form-control'})))
    user = forms.HiddenInput()
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label='Waluta',
                                      widget=(forms.Select({'class': 'form-control'})))
