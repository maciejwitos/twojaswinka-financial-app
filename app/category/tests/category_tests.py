from app.tests.tests import *


class UrlTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@user.com', password='top_secret')

    def create_fake_category(self):
        category = Category.objects.create(name='Kategoria',
                                           user=self.user)
        return category

    def test_category_add_url(self):
        request = self.factory.post('/category/add/')
        request.user = self.user
        response = AddCategory.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_add_new_category_model(self):
        length = Category.objects.count()
        self.create_fake_category()
        assert length + 1 == Category.objects.count()

    def test_category_all_url(self):
        request = self.factory.get('/category/all/')
        request.user = self.user
        response = ReadCategories.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_category_read_model(self):
        category = self.create_fake_category()
        assert category.name == "Kategoria"
        assert category.user == self.user

    def test_category_edit_url(self):
        category = self.create_fake_category()
        request = self.factory.post(f'/category/edit/{category.pk}/')
        request.user = self.user
        response = EditCategory.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_category_edit_model(self):
        category = self.create_fake_category()
        assert category.name == "Kategoria"
        category.name = "Category"
        assert category.name == "Category"


    def test_category_delete_url(self):
        category = create_fake_category()
        request = self.factory.post(f'/category/delete/{category.pk}/')
        request.user = self.user
        response = DeleteCategory.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_category_delete_model(self):
        length = Category.objects.count()
        category = self.create_fake_category()
        assert length + 1 == Category.objects.count()
        category.delete()
        assert length == 0

