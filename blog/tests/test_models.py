from django.test import TestCase

from blog.models import Post, PostCategory, PostComment, PostTag


class TestModels(TestCase):
    def test_adding_post_works(self):
        ...
