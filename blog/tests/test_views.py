from django.test import TestCase
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
