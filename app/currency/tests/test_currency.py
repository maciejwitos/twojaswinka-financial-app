from app.tests.tests import *


class UrlTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@user.com', password='top_secret')

    def create_fake_currency(self):
        currency = Currency.objects.create(name='PLN', in_pln=1)
        return currency

    def test_currency_add_url(self):
        request = self.factory.post('/currency/add/')
        request.user = self.user
        response = AddCurrency.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_add_new_account_model(self):
        length = Currency.objects.count()
        self.create_fake_currency()
        assert length + 1 == Currency.objects.count()

    def test_currency_all_url(self):
        request = self.factory.get('/curreny/all/')
        request.user = self.user
        response = ReadCurrency.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_currency_read_model(self):
        currency = self.create_fake_currency()
        assert currency.name == 'PLN'
        assert currency.in_pln == 1

    def test_currency_edit_model(self):
        currency = self.create_fake_currency()
        assert currency.name == 'PLN'
        currency.name = "GBP"
        assert currency.name == "GBP"

    def test_currency_edit_url(self):
        currency = self.create_fake_currency()
        request = self.factory.post(f'/transaction/edit/{currency.pk}/')
        request.user = self.user
        response = EditCurrency.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_currency_delete_url(self):
        currency = self.create_fake_currency()
        request = self.factory.get('/currency/delete/1')
        request.user = self.user
        response = DeleteCurrency.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_currency_delete_model(self):
        length = Currency.objects.count()
        currency = self.create_fake_currency()
        assert length + 1 == Currency.objects.count()
        currency.delete()
        assert length == 0