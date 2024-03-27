import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Author, Post
import json


class PostsAPITestCase(TestCase):
    def setUp(self):
      self.client = APIClient()
      id1 = uuid.uuid4()
      self.author = Author.objects.create(id=id1, username="test", displayName="test user", url=f"http://localhost:8000/author/{id1}", host="http://localhost:8000/",)
      self.post = Post.objects.create(
        title="Test Post",
        content="This is a test post",
        author=self.author
      )
        

    def test_get_posts(self):
        self.client.force_login(self.author) 
        url = reverse('api_posts', args=[self.author.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['type'], 'posts')
        self.assertEqual(len(response.json()['items']), 1)
        self.assertEqual(response.json()['items'][0]['title'], self.post.title)
        self.assertEqual(response.json()['items'][0]['content'], self.post.content)

    def test_create_post(self):
        url = reverse('api_posts', args=[self.author.id])
        data = {
            'title': 'New Post',
            'content': 'This is a new post',
            'description': 'This is a new post description',
            'author': {
              'id': str(self.author.id),
              'username': self.author.username,
              'displayName': self.author.displayName,
              'url': self.author.url,
              'host': self.author.host
            },
            'type': 'post',
            'contentType': 'text/plain',
            'visibility': 'PUBLIC',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['object']['title'], data['title'])
        self.assertEqual(response.json()['object']['content'], data['content'])


    def test_get_posts_author_not_found(self):
        url = reverse('api_posts', args=[uuid.uuid4()])  # Non-existent author ID
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], 'Author not found')