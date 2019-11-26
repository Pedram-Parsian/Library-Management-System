from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from blog.models import Post


class TestViews(TestCase):
    def test_unpublished_posts_are_not_accessible(self):
        unpublished_post = Post.objects.create(
            title='Sample Draft Post',
            status=Post.DRAFT,
            body='This post has not been published yet!'
        )
        url = reverse('blog:post', kwargs={'slug': unpublished_post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unpublished_posts_are_accessible_for_superusers(self):
        unpublished_post = Post.objects.create(
            title='Sample Draft Post',
            status=Post.DRAFT,
            body='This post has not been published yet!'
        )
        url = reverse('blog:post', kwargs={'slug': unpublished_post.slug})

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='TestAdmin',
            password='qazwsx',
            email='admin@example.com',
            gender=get_user_model().MALE,
        )
        self.client.force_login(self.admin_user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
