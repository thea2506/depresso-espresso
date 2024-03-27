import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Author, LikePost, Post
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
        
    def test_get_posts_no_posts(self):
        id2 = uuid.uuid4()
        author = Author.objects.create(id=id2, username="test2", displayName="test user 2", url=f"http://localhost:8000/author/{id2}", host="http://localhost:8000/",)
        url = reverse('api_posts', args=[author.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['type'], 'posts')
        self.assertEqual(len(response.json()['items']), 0)
        
      

class GetImageTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(username="John", displayName="John Doe")
        self.post = Post.objects.create(author=self.author, contenttype="image/png", content="base64_encoded_image,test")
        self.client.force_login(self.author)

    def test_get_image(self):
        url = reverse('api_get_image', args=[self.author.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
        self.assertEqual(response.content, b'\xb5\xeb-')

    def test_get_image_not_authenticated(self):
        self.client.logout()
        url = reverse('api_get_image', args=[self.author.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"message": "User not authenticated"})

    def test_get_image_author_not_found(self):
        url = reverse('api_get_image', args=[uuid.uuid4(), self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Author not found", "success": False})

    def test_get_image_not_an_image(self):
        non_image_post = Post.objects.create(author=self.author, contenttype="text/plain", content="Hello, world!")
        url = reverse('api_get_image', args=[self.author.id, non_image_post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "Post is not an image", "success": True})

class ApiPostLikeTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(username="John", displayName="John Doe")
        self.post = Post.objects.create(author=self.author, content="Test post")

    def test_api_post_like_get(self):
        url = reverse('api_post_like', args=[self.author.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['type'], 'Like')
        self.assertEqual(len(response.json()['items']), 0)

    def test_api_post_like_method_not_allowed(self):
        url = reverse('api_post_like', args=[self.author.id, self.post.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'detail': 'Method "POST" not allowed.'})
        
        
class ApiLikesTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(username="John", displayName="John Doe", url="http://localhost:8000/author/1", host="http://localhost:8000/")
        self.post = Post.objects.create(author=self.author, content="image_base64_string", contenttype="image/png")

    def test_api_likes(self):
        url = reverse('api_likes', args=[self.author.id, self.post.id])
        data = {
            "author": {
                "url": self.author.url,
                "id": str(self.author.id),
                "displayName": self.author.displayName
            }
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['summary'],  'John Doe liked your post')

        # Check if the like is created
        self.assertTrue(LikePost.objects.filter(author=self.author, post=self.post).exists())

    def test_api_likes_invalid_request(self):
        url = reverse('api_likes', args=[self.author.id, self.post.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.json(),  {'detail': 'Method "GET" not allowed.'})
