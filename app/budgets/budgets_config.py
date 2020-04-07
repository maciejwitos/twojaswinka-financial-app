from app.views import *


class AddBudget(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        form = AddBudgetForm(request.user, initial={'user': request.user})
        return render(request, 'budget/budget_form.html', {'form': form})

    def post(self, request):
        form = AddBudgetForm(request.user, request.POST, initial={'user': request.user})
        if form.is_valid():
            Budget.objects.create(user=request.user,
                                  category=form.cleaned_data['category'],
                                  budget=form.cleaned_data['budget'],
                                  date=form.cleaned_data['date'])
            return redirect('dashboard')
        else:
            return redirect('404')


class ViewBudgets(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):
        budgets = Budget.objects.filter(
                user=request.user).filter(
                date__month=date.today().month).filter(
                date__year=date.today().year)
        return render(request, 'budget/budget_all.html', {'budgets': budgets})

    def post(self, request):
        date_search = request.POST.get('date_search')
        date_search = datetime.datetime.strptime(date_search, '%Y-%m-%d')
        budgets = Budget.objects.filter(
            user=request.user).filter(
            date__month=date_search.month).filter(
            date__year=date_search.year)
        return render(request, 'budget/budget_all.html', {'budgets': budgets})


class DetailsBudget(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, pk):
        budget = Budget.objects.get(id=pk)
        if not request.user.pk == budget.user.pk:
            return redirect('/404/')
        return render(request, 'budget/budget_details.html', {'budget': budget})


class EditBudget(LoginRequiredMixin, UpdateView):

    login_url = '/login/'
    model = Budget
    fields = ('category', 'budget', 'date', 'expenses')
    success_url = '/budget/all/'

    def get(self, request, *args, **kwargs):
        if Budget.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')


class DeleteBudget(LoginRequiredMixin, DeleteView):

    login_url = '/login/'

    model = Budget
    success_url = '/budgets/all/'

    def get(self, request, *args, **kwargs):
        if Budget.objects.get(id=kwargs['pk']).user.pk == request.user.pk:
            return super().get(request, *args, **kwargs)
        return redirect('/404/')