from app.views import *


class AddTransaction(LoginRequiredMixin, View):
    """
    Creating new transaction. At the same time when you add new transaction
    automatically updating account balance, category balance and budget expenses.
    """
    login_url = '/login/'

    def get(self, request):
        """
        :param request:
        :return: AddTransactionForm site
        """
        form = AddTransactionForm(request.user, initial={'user': request.user})
        return render(request, 'transaction/transaction_form.html', {'form': form})

    def post(self, request):
        """

        :param request:
        :return: creating new transaction and updating balances
        """
        form = AddTransactionForm(request.user, request.POST, initial={'user': request.user})
        if form.is_valid():

            # creating new transaction
            Transaction.objects.create(
                date=form.cleaned_data['date'],
                amount=form.cleaned_data['amount'],
                comment=form.cleaned_data['comment'],
                category=form.cleaned_data['category'],
                account=form.cleaned_data['account'],
                is_income=form.cleaned_data['is_income'],
                user=request.user
            )

            # assign transaction amount
            amount = form.cleaned_data['amount']

            # assign boolean value is it income or not
            is_income = form.cleaned_data['is_income']

            # update account balance
            bank = form.cleaned_data['account']
            if is_income:
                bank.balance += amount
            else:
                bank.balance -= amount
            bank.save()

            # update category balance
            category = form.cleaned_data['category']
            category.spending += amount
            category.save()

            """
            Creating budgets is optional so there is a 
            try to update budget expenses if exist
            """

            # assign date of transaction to find correct budget
            transaction_date = form.cleaned_data['date']

            # try to update budget expenses
            try:
                budgets = Budget.objects.filter(
                    user=request.user).filter(
                    category=category).filter(
                    date__month=transaction_date.month).filter(
                    date__year=transaction_date.year)
                budget = Budget.objects.get(id=budgets[0].id)
                budget.expenses += amount
                budget.save()
            except IndexError:
                pass

            return redirect('/transaction/all/')

        # if form is not valid reload to add transaction site
        form = AddTransactionForm(request.user, initial={'user': request.user})
        return render(request, 'transaction/transaction_form.html', {'form': form})


class ReadTransactions(LoginRequiredMixin, View):
    """
    View is loading all transaction for logged user
    """
    login_url = '/login/'

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user.pk).order_by('-date')
        return render(request, 'transaction/transaction_all.html', {'transactions': transactions})


class EditTransaction(LoginRequiredMixin, UpdateView):
    """
    View is updating transaction. Similar to creating transaction
    after submission account and category balances are updating
    as well as budget expenses. If user updates category or account
    class is updating old balances and new category/accounts balances
    """
    login_url = '/login/'

    model = Transaction
    fields = ('date', 'amount', 'account', 'comment', 'category')
    success_url = '/transaction/all/'

    def __init__(self, *args, **kwargs):
        super(EditTransaction, self).__init__(*args, **kwargs)

    # protects user to open other users transaction
    # by typing transaction id straight into url
    def get(self, request, *args, **kwargs):
        if Transaction.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')

    # updates transaction and all balances
    def post(self, request, *args, **kwargs):
        # gets data about editing objects and related models
        transaction = Transaction.objects.get(id=kwargs['pk'])

        # gets date of transaction
        transaction_date = datetime.datetime.strptime(self.get_form().data['date'], '%d.%m.%Y')

        # assign old_budget
        try:
            budgets = Budget.objects.filter(
                user=request.user).filter(
                category=transaction.category).filter(
                date__month=transaction_date.month).filter(
                date__year=transaction_date.year)
            old_budget = Budget.objects.get(id=budgets[0].id)
            old_budget.expenses -= transaction.amount
            old_budget.save()
        except IndexError:
            pass

        # updates old balances for accounts, category and budgets
        if transaction.is_income:
            transaction.account.balance -= transaction.amount
        else:
            transaction.account.balance += transaction.amount
        transaction.category.spending -= transaction.amount

        # saves updated models
        transaction.account.save()
        transaction.category.save()

        # assing new category, account and budget according changes in form
        new_category = Category.objects.get(id=self.get_form().data['category'])
        new_account = Account.objects.get(id=self.get_form().data['account'])

        # takes new amount from form
        new_amount = float(self.request.POST.get('amount'))

        try:
            budgets = Budget.objects.filter(
                user=request.user).filter(
                category=new_category).filter(
                date__month=transaction_date.month).filter(
                date__year=transaction_date.year)
            new_budget = Budget.objects.get(id=budgets[0].id)
            new_budget.expenses += Decimal(new_amount)
            new_budget.save()
        except IndexError:
            pass

        # updates new category, account and budget balances
        if transaction.is_income:
            new_account.balance += Decimal(new_amount)
        else:
            new_account.balance -= Decimal(new_amount)
        new_category.spending += Decimal(new_amount)

        # saves models
        new_account.save()
        new_category.save()

        return super().post(request, *args, **kwargs)


class DeleteTransaction(LoginRequiredMixin, DeleteView):
    """
    Delete transaction form database and updates all connected models
    """
    login_url = '/login/'

    model = Transaction
    success_url = reverse_lazy('/transaction/all/')

    # protects user to open other users transaction
    # by typing transaction id straight into url
    def get(self, request, *args, **kwargs):
        if Transaction.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')

    def delete(self, request, *args, **kwargs):
        # gets data about deleted objects and related models
        transaction = Transaction.objects.get(id=kwargs['pk'])

        # gets data about account, category and budget
        bank = transaction.account
        category = transaction.category
        try:
            budgets = Budget.objects.filter(
                user=request.user).filter(
                category=transaction.category).filter(
                date__month=transaction.date.month).filter(
                date__year=transaction.date.year)
            budget = Budget.objects.get(id=budgets[0].id)
        except IndexError:
            pass
        # delete object
        result = super().delete(request, *args, **kwargs)

        # refunds for category, account and budget balances
        if category is not None:
            category.spending -= transaction.amount
            category.save()
        if bank is not None:
            if transaction.is_income:
                bank.balance -= transaction.amount
            else:
                bank.balance += transaction.amount
            bank.save()
        try:
            if budget is not None:
                budget.expenses -= transaction.amount
                budget.save()
        except:
            pass

        return result
