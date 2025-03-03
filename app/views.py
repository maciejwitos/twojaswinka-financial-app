from django.db.models import Q
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView
from app.user.user_forms import SignUpForm
from app.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import DeletionMixin
from django.http import HttpResponse
from app.accounts.accounts_forms import *
from datetime import date
from app.budgets.budgets_form import *
from app.category.category_forms import *
from app.currency.currency_form import *
from app.transactions.transaction_form import AddTransactionForm
from decimal import Decimal
from app.category.category_config import *
from scraper.update_currencies_values import read_values


class HomePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'homepage.html')


class Dashboard(LoginRequiredMixin, View):

    login_url = '/login/'

    def get(self, request):

        last_update = LastUpdateDate.objects.get(id=1)
        if not last_update.last_update == date.today():
            read_values()
            last_update.last_update = date.today()
            last_update.save()

        currencies = Currency.objects.all()
        transactions = Transaction.objects.filter(
            user=request.user).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year).order_by('-date')
        accounts = Account.objects.filter(user=request.user).order_by('-balance')
        budgets = Budget.objects.filter(
            user=request.user).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year).order_by('-expenses')

        my_wealth = 0
        for account in accounts:
            balance = account.balance
            balance_in_pln = balance * account.currency.in_pln
            my_wealth += balance_in_pln

        monthly_spending = 0
        monthly_budget = 0

        for budget in budgets:
            category_budget = budget.budget
            expenses = budget.expenses
            monthly_spending += expenses
            monthly_budget += category_budget
        return render(request, 'dashboard.html', {'currencies': currencies,
                                                  'transactions': transactions,
                                                  'accounts': accounts,
                                                  'budgets': budgets,
                                                  'my_wealth': round(my_wealth, 2),
                                                  'monthly_spending': monthly_spending,
                                                  'monthly_budget': monthly_budget})

    def post(self, request):
        data = request.POST.get('search_transaction')
        currencies = Currency.objects.all()
        # search for transaction
        transactions = Transaction.objects.filter(user=request.user).filter(
            Q(comment__icontains=data) | Q(date__icontains=data)).order_by('-date')

        accounts = Account.objects.filter(user=request.user).order_by('-balance')
        budgets = Budget.objects.filter(
            user=request.user).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year).order_by('-expenses')

        my_wealth = 0
        for account in accounts:
            balance = account.balance
            balance_in_pln = balance * account.currency.in_pln
            my_wealth += balance_in_pln
        return render(request, 'dashboard.html', {'currencies': currencies,
                                                  'budgets': budgets,
                                                  'transactions': transactions,
                                                  'accounts': accounts,
                                                  'my_wealth': round(my_wealth, 2)})


class View404(View):
    """
    View for redirection after error
    """
    def get(self, request):
        return render(request, '404.html')
