from app.forms import *


class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('date', 'amount', 'comment', 'category', 'account', 'user', )

    def __init__(self, user, *args, **kwargs):
        super(AddTransactionForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget=forms.TextInput({'class':'form-control'})
        self.fields['comment'].label='Komentarz'
        self.fields['amount'].widget=forms.NumberInput({'class':'form-control'})
        self.fields['amount'].label='Kwota'
        self.fields['date'].widget=forms.SelectDateWidget({'class':"form-control"})
        self.fields['date'].label='Data'
        self.fields['category'].widget=forms.Select({'class':'form-control select2'})
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].label='Kategoria'
        self.fields['account'].widget = forms.Select({'class': 'form-control select2'})
        self.fields['account'].queryset=Account.objects.filter(user=user)
        self.fields['account'].label = 'Konto'
        self.fields['user'].widget=forms.HiddenInput()