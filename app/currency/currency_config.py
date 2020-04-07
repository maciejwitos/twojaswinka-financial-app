from app.views import *


class AddCurrency(PermissionRequiredMixin, View):
    permission_required = 'app/add_logentry'

    def handle_no_permission(self):
        return redirect('404')

    def get(self, request):
        form = AddCurrencyForm()
        return render(request, 'currency/currency_form.html', {"form": form})

    def post(self, request):
        form = AddCurrencyForm(request.POST)
        if form.is_valid():
            Currency.objects.create(
                name=form.cleaned_data['name'],
                in_pln=form.cleaned_data['in_pln']
            )
            return redirect('all-currency')
        return redirect('all-currency')


class ReadCurrency(PermissionRequiredMixin, View):
    permission_required = 'app/add_logentry'

    def get(self, request):
        currencies = Currency.objects.all()
        return render(request, 'currency/currency_all.html', {"currencies": currencies})


class EditCurrency(PermissionRequiredMixin, UpdateView):
    permission_required = 'app/add_logentry'

    def handle_no_permission(self):
        return redirect('404')

    model = Currency
    fields = ('name', 'in_pln')
    success_url = '/currency/all/'


class DeleteCurrency(PermissionRequiredMixin, DeleteView):
    permission_required = 'app/add_logentry'

    def handle_no_permission(self):
        return redirect('404')

    model = Currency
    success_url = reverse_lazy('/currency/all/')
