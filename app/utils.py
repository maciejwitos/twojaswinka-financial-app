import pytest
from app.models import *
from faker import Faker

fake = Faker()


@pytest.mark.django_db
def fake_user():
    user = User.objects.create(username=fake.first_name_male())
    return user


@pytest.mark.django_db
def fake_currency():
    currency = Currency.objects.create(name=fake.currency_code(),
                                       in_pln=1)
    return currency


@pytest.mark.django_db
def fake_category():
    category = Category.objects.create(name=fake.safe_color_name(),
                                       user=fake_user())
    return category


@pytest.mark.django_db
def fake_account():
    account = Account.objects.create(bank=fake.company(),
                                     name=fake.first_name_male(),
                                     balance=999,
                                     currency=fake_currency(),
                                     user=fake_user())
    return account


@pytest.mark.django_db
def fake_budget():
    budget = Budget.objects.create(category=fake_category(),
                                   budget=999,
                                   date=fake.date(),
                                   user=fake_user())
    return budget


@pytest.mark.django_db
def fake_transaction():
    transaction = Transaction.objects.create(date=fake.date(),
                                             comment=fake.name(),
                                             amount=999,
                                             account=fake_account(),
                                             category=fake_category(),
                                             user=fake_user())
    return transaction
