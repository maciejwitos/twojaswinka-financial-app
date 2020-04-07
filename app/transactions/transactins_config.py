from app.views import *


# Dodawanie transakcji
class AddTransaction(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        form = AddTransactionForm(request.user, initial={'user': request.user})
        return render(request, 'transaction/transaction_form.html', {'form': form})

    def post(self, request):
        form = AddTransactionForm(request.user, request.POST, initial={'user': request.user})
        if form.is_valid():
            Transaction.objects.create(
                date=form.cleaned_data['date'],
                amount=form.cleaned_data['amount'],
                comment=form.cleaned_data['comment'],
                category=form.cleaned_data['category'],
                account=form.cleaned_data['account'],
                user=request.user
            )

            amount = form.cleaned_data['amount']

            bank = form.cleaned_data['account']
            bank.balance -= amount
            bank.save()

            category = form.cleaned_data['category']
            category.spending += amount
            category.save()
            try:
                budgets = Budget.objects.filter(
                    user=request.user).filter(
                    category=category).filter(
                    date__month=date.today().month).filter(
                    date__year=date.today().year)
                budget = Budget.objects.get(id=budgets[0].id)
                budget.expenses += amount
                budget.save()
            except IndexError:
                pass

            return redirect('/transaction/all/')

        form = AddTransactionForm(request.user, initial={'user': request.user})
        return render(request, 'transaction/transaction_form.html', {'form': form})


# Wypisanie wszystkich transakcji
class ReadTransactions(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user.pk).order_by('-date')
        return render(request, 'transaction/transaction_all.html', {'transactions': transactions})


class EditTransaction(LoginRequiredMixin, UpdateView):
    login_url = '/login/'

    model = Transaction
    fields = ('date', 'amount', 'category', 'account', 'comment')
    success_url = '/transaction/all/'

    def __init__(self, *args, **kwargs):
        super(EditTransaction, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        if Transaction.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')

    def post(self, request, *args, **kwargs):
        # get data about editing objects and related models
        transaction = Transaction.objects.get(id=kwargs['pk'])
        budgets = Budget.objects.filter(
            user=request.user).filter(
            category=transaction.category).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year)
        budget = Budget.objects.get(id=budgets[0].id)
        # subtract old amount from category spending, account balance and budget expenses
        transaction.account.balance += transaction.amount
        transaction.category.spending -= transaction.amount
        budget.expenses -= transaction.amount
        # take new amount from form
        new_amount = float(self.request.POST.get('amount'))
        # add new amount to cateogry spending and account balance
        transaction.category.spending += Decimal(new_amount)
        transaction.account.balance -= Decimal(new_amount)
        budget.expenses += Decimal(new_amount)
        # save models
        transaction.account.save()
        transaction.category.save()
        budget.save()
        return super().post(request, *args, **kwargs)


# Usuwanie transakcji
class DeleteTransaction(LoginRequiredMixin, DeleteView):
    login_url = '/login/'

    model = Transaction
    success_url = reverse_lazy('/transaction/all/')

    def get(self, request, *args, **kwargs):
        if Transaction.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')

    def delete(self, request, *args, **kwargs):
        # get data about deleted objects and related models
        transaction = Transaction.objects.get(id=kwargs['pk'])
        bank = transaction.account
        category = transaction.category
        budgets = Budget.objects.filter(
            user=request.user).filter(
            category=transaction.category).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year)
        budget = Budget.objects.get(id=budgets[0].id)
        # delete object
        result = super().delete(request, *args, **kwargs)
        # refund for category and account balance
        if category is not None:
            category.spending -= transaction.amount
            category.save()
        if bank is not None:
            bank.balance += transaction.amount
            bank.save()
        if budget is not None:
            budget.expenses -= transaction.amount
            budget.save()

        return result




