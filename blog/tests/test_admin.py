from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='TestAdmin',
            password='qazwsx',
            email='admin@example.com',
            gender=get_user_model().MALE,
        )
        self.client.force_login(self.admin_user)

    def test_admin_posts_list_page_works(self):
        """Test that the posts list page in the admin renders correctly"""
        url = reverse('admin:blog_post_changelist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
