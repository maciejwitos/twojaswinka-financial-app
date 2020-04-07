from app.forms import *


class AddBudgetForm(forms.ModelForm):

    class Meta:

        model = Budget
        fields = ('user', 'category', 'budget', 'date', 'expenses', )

    def __init__(self, user, *args, **kwargs):
        super(AddBudgetForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['category'].widget = forms.Select({'class': 'form-control select2'})
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].label = 'Kategoria'
        self.fields['date'].widget=forms.SelectDateWidget({'class':"form-control"})
        self.fields['date'].label='Data'
        self.fields['budget'].widget=forms.NumberInput({'class':'form-control'})
        self.fields['budget'].label='Budżet'
        self.fields['expenses'].widget = forms.HiddenInput()