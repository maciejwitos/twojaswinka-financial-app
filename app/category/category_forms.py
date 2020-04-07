from app.forms import *


class AddCategoryForm(forms.Form):
    name = forms.CharField(max_length=24, label='Nazwa', widget=forms.TextInput({'class':'form-control'}))
    spending = forms.HiddenInput()
    user = forms.HiddenInput()