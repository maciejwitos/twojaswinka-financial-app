from app.views import *


# Dodawanie nowego konta
class AddAccount(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = AddAccountForm()
        return render(request, 'account/account_form.html', {'form': form})

    def post(self, request):
        form = AddAccountForm(request.POST)
        if form.is_valid():
            Account.objects.create(
                name=form.cleaned_data['name'],
                bank=form.cleaned_data['bank'],
                currency=form.cleaned_data['currency'],
                balance=form.cleaned_data['balance'],
                user=request.user
            )
            return redirect('all-account')
        return redirect('all-account')


# Wyświetlanie wszystkich kont
class ReadAccounts(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        accounts = Account.objects.filter(user=request.user.pk).order_by('name')
        return render(request, 'account/account_all.html', {'accounts': accounts})


# Edycja konta
class EditAccount(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    model = Account
    fields = ('name', 'bank', 'currency', 'balance', 'user',)
    success_url = '/account/all/'

    def get(self, request, *args, **kwargs):
        if Account.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')


class DetailsAccount(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        account = Account.objects.get(id=pk)
        transactions = Transaction.objects.filter(account=account)
        if not request.user.pk == account.user.pk:
            return redirect('/404/')
        return render(request, 'account/account_details.html', {'account': account,
                                                                'transactions': transactions})


# Usuwanie konta
class DeleteAccount(LoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = Account
    success_url = '/account/all/'

    def get(self, request, *args, **kwargs):
        if Account.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')


