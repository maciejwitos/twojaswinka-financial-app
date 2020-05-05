from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from app.models import *
from app.utils import *
from django.test import Client
from app.views import Dashboard

client = Client()


def test_view_dashboard_get():
    response = client.get('/dashboard/')
    assert response.status_code == 302


def test_view_dashboard_post():
    response = client.post('/dashboard/')
    assert response.status_code == 302


def test_view_404_get():
    response = client.get('/404/')
    assert response.status_code == 200


def test_view_login_get():
    response = client.get('/login/')
    assert response.status_code == 200


def test_view_login_post():
    response = client.post('/login/')
    assert response.status_code == 200


def test_view_register_get():
    response = client.get('/register/')
    assert response.status_code == 200


def test_view_register_post():
    response = client.post('/register/')
    assert response.status_code == 200


def test_view_logout_get():
    response = client.get('/logout/')
    assert response.status_code == 200


def test_view_logout_post():
    response = client.post('/logout/')
    assert response.status_code == 200


def test_view_password_change_get():
    response = client.get('/password_change/')
    assert response.status_code == 302


def test_view_password_change_post():
    response = client.post('/password_change/')
    assert response.status_code == 302


def test_view_password_change_done_get():
    response = client.get('/password_change/done/')
    assert response.status_code == 302


def test_view_password_change_done_post():
    response = client.post('/password_change/done/')
    assert response.status_code == 302


def test_view_password_reset_get():
    response = client.get('/password_reset/')
    assert response.status_code == 200


def test_view_user_details_get():
    response = client.get('/details/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_user_delete_get():
    user = fake_user()
    response = client.get(f'/user/delete/{user.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_user_delete_post():
    user = fake_user()
    response = client.post(f'/user/delete/{user.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_add_get():
    response = client.get('/category/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_add_post():
    response = client.post('/category/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_all_get():
    response = client.get('/category/all/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_add_get():
    response = client.get('/category/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_details_get():
    category = fake_category()
    response = client.get(f'/category/details/{category.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_edit_get():
    category = fake_category()
    response = client.get(f'/category/edit/{category.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_edit_post():
    category = fake_category()
    response = client.post(f'/category/edit/{category.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_delete_get():
    category = fake_category()
    response = client.get(f'/category/delete/{category.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_category_delete_post():
    category = fake_category()
    response = client.post(f'/category/delete/{category.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_add_get():
    response = client.get('/currency/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_add_post():
    response = client.post('/currency/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_all_get():
    response = client.post('/currency/all/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_edit_get():
    currency = fake_currency()
    response = client.get(f'/currency/edit/{currency.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_edit_post():
    currency = fake_currency()
    response = client.post(f'/currency/edit/{currency.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_delete_get():
    currency = fake_currency()
    response = client.get(f'/currency/delete/{currency.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_currency_edit_post():
    currency = fake_currency()
    response = client.post(f'/currency/delete/{currency.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_add_get():
    response = client.get('/account/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_add_post():
    response = client.post('/account/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_all_get():
    response = client.get('/account/all/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_details_get():
    account = fake_account()
    response = client.get(f'/account/details/{account.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_edit_get():
    account = fake_account()
    response = client.get(f'/account/edit/{account.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_edit_post():
    account = fake_account()
    response = client.post(f'/account/edit/{account.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_delete_get():
    account = fake_account()
    response = client.get(f'/account/delete/{account.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_account_delete_post():
    account = fake_account()
    response = client.post(f'/account/delete/{account.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_add_get():
    response = client.get('/budget/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_add_post():
    response = client.post('/budget/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_all_get():
    response = client.get('/budget/all/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_details_get():
    budget = fake_budget()
    response = client.get(f'/budget/details/{budget.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_edit_get():
    budget = fake_budget()
    response = client.get(f'/budget/edit/{budget.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_edit_post():
    budget = fake_budget()
    response = client.post(f'/budget/edit/{budget.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_delete_get():
    budget = fake_budget()
    response = client.get(f'/budget/delete/{budget.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_budget_delete_post():
    budget = fake_budget()
    response = client.post(f'/budget/delete/{budget.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_add_get():
    response = client.get('/transaction/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_add_post():
    response = client.post('/transaction/add/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_all_get():
    response = client.get('/transaction/all/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_edit_get():
    transaction = fake_transaction()
    response = client.get(f'/transaction/edit/{transaction.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_edit_post():
    transaction = fake_transaction()
    response = client.post(f'/transaction/edit/{transaction.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_delete_get():
    transaction = fake_transaction()
    response = client.get(f'/transaction/delete/{transaction.pk}/')
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_transaction_delete_post():
    transaction = fake_transaction()
    response = client.post(f'/transaction/delete/{transaction.pk}/')
    assert response.status_code == 302


