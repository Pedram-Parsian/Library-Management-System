from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_POST_URL = reverse('blog:create')


#
# def create_post(**kwargs):
#     return get_user_model()

class PublicPostApiTests(TestCase):
    """Test the post API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_post_fails(self):
        """Test creating post with valid payload fails"""
        payload = {

        }
        res = self.client.post(CREATE_POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivatePostApiTests(TestCase):
    """Test the post API (private)"""

    def setUp(self) -> None:
        # authenticate
        self.client = APIClient()
