import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Post
from authentication.models import Author, Following
from .serializers import AuthorSerializer, PostSerializer

class PostsAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(username='test_author', password='test_password')
        self.author2 = Author.objects.create(username='test_author2', password='test_password2')
        self.post = Post.objects.create(title='Test Post', author=self.author, description='Test Description', contentType='text/plain', content='Test Content', visibility='PUBLIC')

    def test_api_posts_get_authenticated_author(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('get_author_posts', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['type'], 'post')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Post')

    def test_api_posts_get_friend_author(self):
        Following.objects.create(authorid=self.author, followingid=self.author2)
        Following.objects.create(authorid=self.author2, followingid=self.author)
        self.client.force_login(self.author2)
        response = self.client.get(reverse('api_get_posts', args=[self.author.id]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'posts')
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['title'], 'Test Post')
