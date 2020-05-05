from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from app.models import *
from app.utils import *


#################   TESTS FOR CREATE MODELS   ####################
@pytest.mark.django_db
def test_create_user():
    elements_in_database = User.objects.count()
    user = User.objects.create(username='random')

    assert User.objects.count() == elements_in_database + 1
    assert user.pk == 1
    assert user.is_anonymous == False


@pytest.mark.django_db
def test_create_category():
    elements_in_database = Category.objects.count()
    user = fake_user()
    category = Category.objects.create(name='category',
                                       user=user)

    assert Category.objects.count() == elements_in_database + 1
    assert category.name == 'category'
    assert category.user.pk == 2


@pytest.mark.django_db
def test_create_account():
    elements_in_database = Account.objects.count()
    account = Account.objects.create(name='my_account')

    assert Account.objects.count() == elements_in_database + 1
    assert account.name == 'my_account'
    assert account.pk == 1
    assert account.currency is None
    assert account.balance == 0


@pytest.mark.django_db
def test_create_budget():
    elements_in_database = Budget.objects.count()
    category = fake_category()
    budget = Budget.objects.create(budget=100,
                                   category=category,
                                   date='2020-02-01')

    assert Budget.objects.count() == elements_in_database + 1
    assert budget.budget == 100
    assert budget.category.pk == category.pk
    assert budget.date == '2020-02-01'
    assert budget.user is None


@pytest.mark.django_db
def test_create_transaction():
    elements_in_database = Transaction.objects.count()
    account = Account.objects.create(name='my_account')
    category = fake_category()
    transactions = Transaction.objects.create(amount=12.49,
                                              account_id=account.pk,
                                              category_id=category.pk,
                                              date='2020-02-01')

    assert Transaction.objects.count() == elements_in_database + 1
    assert transactions.pk == 1
    assert transactions.account == account


@pytest.mark.django_db
def test_create_currency():
    elements_in_database = Currency.objects.count()
    currency = Currency.objects.create(name='AAA',
                                       in_pln=1)

    assert Currency.objects.count() == elements_in_database + 1
    assert currency.pk == 1
    assert currency.in_pln == 1


#################   TESTS FOR DELETE MODELS   ####################
@pytest.mark.django_db
def test_delete_user():
    user = fake_user()
    elements_in_database_before_deletion = User.objects.count()
    user.delete()
    assert User.objects.count() == elements_in_database_before_deletion - 1


@pytest.mark.django_db
def test_delete_category():
    category = fake_category()
    elements_in_database_before_deletion = Category.objects.count()
    category.delete()
    assert Category.objects.count() == elements_in_database_before_deletion - 1


@pytest.mark.django_db
def test_delete_currency():
    currency = fake_currency()
    elements_in_database_before_deletion = Currency.objects.count()
    currency.delete()
    assert Currency.objects.count() == elements_in_database_before_deletion - 1


@pytest.mark.django_db
def test_delete_account():
    account = fake_account()
    elements_in_database_before_deletion = Account.objects.count()
    account.delete()
    assert Account.objects.count() == elements_in_database_before_deletion - 1


@pytest.mark.django_db
def test_delete_budget():
    budget = fake_budget()
    elements_in_database_before_deletion = Budget.objects.count()
    budget.delete()
    assert Budget.objects.count() == elements_in_database_before_deletion - 1


@pytest.mark.django_db
def test_delete_transaction():
    transaction = fake_transaction()
    elements_in_database_before_deletion = Transaction.objects.count()
    transaction.delete()
    assert Transaction.objects.count() == elements_in_database_before_deletion - 1


#################   TESTS FOR EDIT MODELS   ####################
@pytest.mark.django_db
def test_edit_user():
    user = fake_user()
    old_user_name = user.username
    user.username = 'new_name'
    assert user.username != old_user_name
    assert user.username == 'new_name'


@pytest.mark.django_db
def test_edit_currency():
    currency = fake_currency()
    old_currency_name = currency.name
    currency.name = 'new_name'
    assert currency.name != old_currency_name
    assert currency.name == 'new_name'


@pytest.mark.django_db
def test_edit_category():
    category = fake_category()
    old_category_name = category.name
    category.name = 'new_name'
    assert category.name != old_category_name
    assert category.name == 'new_name'


@pytest.mark.django_db
def test_edit_account():
    account = fake_account()
    old_account_name = account.name
    account.name = 'new_name'
    assert account.name != old_account_name
    assert account.name == 'new_name'


@pytest.mark.django_db
def test_edit_budget():
    budget = fake_budget()
    old_budget_budget = budget.budget
    budget.budget = 888
    assert budget.budget != old_budget_budget
    assert budget.budget == 888


@pytest.mark.django_db
def test_edit_transaction():
    transaction = fake_transaction()
    old_transaction_name = transaction.comment
    transaction.comment = 'new_comment'
    assert transaction.comment != old_transaction_name
    assert transaction.comment == 'new_comment'






