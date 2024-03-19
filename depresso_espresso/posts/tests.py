import unittest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Post, Comment, Author

class PostTests(TestCase):
    def setUp(self):
      self.user = Author.objects.create_user(username='testuser', password='testpassword')
      self.client.login(username='testuser', password='testpassword')

    def test_new_post(self):
      response = self.client.post('new_post', {
        'title': 'Test Post',
        'visibility': 'PUBLIC',
        'description': 'This is a test post',
        'contentType': 'text/plain',
        'content': 'Hello, world!'
      })
      self.assertEqual(response.status_code, 400)
      self.assertTrue('success' in response.json())
      self.assertTrue('id' in response.json())


if __name__ == '__main__':
    unittest.main()