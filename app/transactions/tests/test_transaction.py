from app.tests.tests import *


class UrlTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@user.com', password='top_secret')

    def create_fake_transaction(self):
        transaction = Transaction.objects.create(date='2020-03-03',
                                                 user=self.user,
                                                 account=create_fake_account(),
                                                 category=create_fake_category(),
                                                 comment='fake_comment',
                                                 amount=150)
        return transaction

    def test_transaction_add_url(self):
        request = self.factory.get('/transaction/add/')
        request.user = self.user
        response = AddTransaction.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_add_new_transaction_model(self):
        length = Transaction.objects.count()
        self.create_fake_transaction()
        assert length + 1 == Transaction.objects.count()

    def test_transaction_all_url(self):
        request = self.factory.get('/transactions/all/')
        request.user = self.user
        response = ReadTransactions.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_transaction_read_model(self):
        transaction = self.create_fake_transaction()
        assert transaction.date == '2020-03-03'
        assert transaction.amount == 150

    def test_transaction_edit_model(self):
        transaction = self.create_fake_transaction()
        assert transaction.date == '2020-03-03'
        transaction.name = '2020-10-10'
        assert transaction.name == '2020-10-10'

    def test_transaction_edit_url(self):
        transaction = self.create_fake_transaction()
        request = self.factory.post(f'/transaction/edit/{transaction.pk}/')
        request.user = self.user
        response = EditTransaction.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_transaction_delete_url(self):
        transaction = self.create_fake_transaction()
        request = self.factory.post(f'/transaction/delete/{transaction.pk}/')
        request.user = self.user
        response = DeleteTransaction.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_transaction_delete_model(self):
        length = Transaction.objects.count()
        transaction = self.create_fake_transaction()
        assert length + 1 == Transaction.objects.count()
        transaction.delete()
        assert length == 0
