from app.tests.tests import *
from app.currency.tests.test_currency import TestCase


class UrlTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@user.com', password='top_secret')

    def create_fake_account(self):
        account = Account.objects.create(name='fake_bank_name',
                                         bank='fake_bank',
                                         balance=100,
                                         currency=create_fake_currency(),
                                         user=self.user)
        return account

    def test_account_add_url(self):
        request = self.factory.post('/account/add/')
        request.user = self.user
        response = AddAccount.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_add_new_account_model(self):
        length = Account.objects.count()
        self.create_fake_account()
        assert length + 1 == Account.objects.count()

    def test_account_all_url(self):
        request = self.factory.get('/account/all/')
        request.user = self.user
        response = ReadAccounts.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_account_read_model(self):
        account = self.create_fake_account()
        assert account.name == 'fake_bank_name'
        assert account.user == self.user
        assert account.bank == 'fake_bank'

    def test_account_edit_url(self):
        account = self.create_fake_account()
        request = self.factory.post(f'/category/edit/{account.pk}/')
        request.user = self.user
        response = EditAccount.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_account_edit_model(self):
        account = self.create_fake_account()
        assert account.name == 'fake_bank_name'
        account.name = "new_fake_name"
        assert account.name == "new_fake_name"

    def test_account_delete_url(self):
        account = self.create_fake_account()
        request = self.factory.post(f'/account/delete/{account.pk}', data={'name': account.name,
                                                                           'bank': account.bank,
                                                                           'currency': account.currency,
                                                                           'user': account.user,
                                                                           'balance': account.balance})
        request.user = account.user
        response = DeleteAccount.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_account_delete_model(self):
        length = Account.objects.count()
        account = self.create_fake_account()
        assert length + 1 == Account.objects.count()
        account.delete()
        assert length == 0
