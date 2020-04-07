from app.tests.tests import *
from app.models import *
from faker import Faker

faker = Faker()


def get_random_user():
    user = User.objects.create_user(
        username=faker.name(), email='test@test.pl', password='top_secret')
    return user


def create_fake_account():
    account = Account.objects.create(name='fake_bank_name',
                                     bank='fake_bank',
                                     balance=100,
                                     currency=create_fake_currency(),
                                     user=get_random_user())
    return account


def create_fake_currency():
    currency = Currency.objects.create(name='PLN', in_pln=1)
    return currency


def create_fake_category():
    category = Category.objects.create(name='Kategoria',
                                       user=get_random_user())
    return category
