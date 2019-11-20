from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from blog.models import Post


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

        self.post = Post.objects.create(
            title='Test Post',
            status=Post.DRAFT,
            body='Just testing...'
        )

    def test_admin_posts_changelist_page_works(self):
        """Test that the posts changelist page in the admin renders correctly"""
        url = reverse('admin:blog_post_changelist')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_admin_posts_add_page_works(self):
        """Test that the posts add page in the admin renders correctly"""
        url = reverse('admin:blog_post_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_admin_posts_history_page_works(self):
        """Test that the posts history page in the admin renders correctly"""
        url = reverse('admin:blog_post_history', args=[self.post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_admin_posts_delete_page_works(self):
        """Test that the posts delete page in the admin renders correctly"""
        url = reverse('admin:blog_post_delete', args=[self.post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_admin_posts_change_page_works(self):
        """Test that the posts change page in the admin renders correctly"""
        url = reverse('admin:blog_post_change', args=[self.post.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
