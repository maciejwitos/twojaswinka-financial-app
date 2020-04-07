from django.db.models import Q
from app.currency.scraper.currency_scraper import *
from django.views.generic import UpdateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView
from app.forms import SignUpForm
from app.models import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import DeletionMixin
from django.http import HttpResponse
from app.accounts.accounts_forms import *
import datetime
from app.budgets.budgets_form import *
from app.category.category_forms import *
from app.currency.currency_form import *
from app.transactions.transaction_form import AddTransactionForm
from decimal import Decimal
from app.user.user_config import *
from app.budgets.budgets_config import *
from app.category.category_config import *
from app.accounts.accounts_config import *
from app.transactions.transactins_config import *
from app.currency.currency_config import *


class Dashboard(LoginRequiredMixin, View):
    """
    Main View Dashboard. When run it's:
    - updating currencies
    - showing all sections for user: categories, currencies, transactions and accounts
    - has search for transactions
    - showing total wealth of user
    """
    login_url = '/login/'

    def get(self, request):
        GetCurrencies.scrap_currencies(current_day=date.today())
        categories = Category.objects.filter(user=request.user).order_by('-spending')
        currencies = Currency.objects.all()
        transactions = Transaction.objects.filter(
            user=request.user).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year).order_by('-date')
        accounts = Account.objects.filter(user=request.user).order_by('-balance')
        budgets = Budget.objects.filter(
            user=request.user).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year)
        my_wealth = 0
        for account in accounts:
            balance = account.balance
            balance_in_pln = balance * account.currency.in_pln
            my_wealth += balance_in_pln
        return render(request, 'dashboard.html', {'categories': categories,
                                                  'currencies': currencies,
                                                  'transactions': transactions,
                                                  'accounts': accounts,
                                                  'budgets': budgets,
                                                  'my_wealth': float(my_wealth)})

    def post(self, request):
        data = request.POST.get('search_transaction')
        categories = Category.objects.filter(user=request.user).order_by('-spending')
        currencies = Currency.objects.all()
        # search for transaction
        transactions = Transaction.objects.filter(user=request.user).filter(
            Q(comment__icontains=data) | Q(date__icontains=data)).order_by('-date')

        accounts = Account.objects.filter(user=request.user).order_by('-balance')
        budgets = Budget.objects.filter(
            user=request.user).filter(
            date__month=date.today().month).filter(
            date__year=date.today().year)

        my_wealth = 0
        for account in accounts:
            balance = account.balance
            balance_in_pln = balance * account.currency.in_pln
            my_wealth += balance_in_pln
        return render(request, 'dashboard.html', {'categories': categories,
                                                  'currencies': currencies,
                                                  'budgets': budgets,
                                                  'transactions': transactions,
                                                  'accounts': accounts,
                                                  'my_wealth': float(my_wealth)})


class View404(View):
    """
    View for redirection after error
    """
    def get(self, request):
        return render(request, '404.html')
