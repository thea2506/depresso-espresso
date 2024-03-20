import json
import uuid
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post
from authentication.models import Author


class PostsAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(username='test_author', password='test_password')
        self.author2 = Author.objects.create(username='test_author2', password='test_password2')
        self.post = Post.objects.create(title='Test Friend Post', author=self.author, description='Test Friend Description', contentType='text/plain', content='Test Friend Content', visibility='FRIENDS')
        self.post = Post.objects.create(title='Test Public Post', author=self.author2, description='Test Description', contentType='text/plain', content='Test Content', visibility='PUBLIC')

    def test_api_posts_get_authenticated_author(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('get_author_posts', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['type'], 'post')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Friend Post')

    def test_api_posts_get_public_author(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('api_get_posts', args=[self.author2.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'posts')
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['title'], 'Test Public Post')

    def test_api_posts_get_author_not_found(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('api_get_posts', args=[uuid.uuid4()]))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Author not found')
        self.assertFalse(data['success'])

    def test_api_posts_get_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get(reverse('api_get_posts', args=[self.author.id]))
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'User not authenticated')

    def test_api_posts_post_authenticated_author(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('api_get_posts', args=[self.author.id]), {
            'title': 'New Post',
            'description': 'New Description',
            'contentType': 'text/plain',
            'content': 'New Content',
            'visibility': 'PUBLIC'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Post created')
        self.assertTrue(data['success'])
        self.assertEqual(data['object']['title'], 'New Post')

    def test_api_posts_post_unauthenticated_user(self):
        self.client.logout()
        response = self.client.post(reverse('api_get_posts', args=[self.author.id]), {
            'title': 'New Post',
            'description': 'New Description',
            'contentType': 'text/plain',
            'content': 'New Content',
            'visibility': 'PUBLIC'
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'User not authenticated')

    def test_api_posts_post_local_user(self):
        self.client.force_login(self.author2)
        response = self.client.post(reverse('api_get_posts', args=[self.author.id]), {
            'title': 'New Post',
            'description': 'New Description',
            'contentType': 'text/plain',
            'content': 'New Content',
            'visibility': 'PUBLIC'
        })
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Local users only')

    def test_api_posts_post_invalid_form(self):
        self.client.force_login(self.author)
        response = self.client.post(reverse('api_get_posts', args=[self.author.id]), {
            'title': 'New Post',
            'description': 'New Description',
            'contentType': 'text/plain',
            'content': '',  # Invalid form, content is empty
            'visibility': 'PUBLIC'
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Invalid form')
        self.assertFalse(data['success'])

    def test_api_posts_post_method_not_allowed(self):
        self.client.force_login(self.author)
        response = self.client.put(reverse('api_get_posts', args=[self.author.id]))
        self.assertEqual(response.status_code, 405)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Method not allowed')