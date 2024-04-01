from django.urls import reverse
import json
import uuid
from django.test import TestCase, Client
from authentication.models import Author, Following
from authentication.serializers import AuthorSerializer


class AuthorsAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        id1 = uuid.uuid4()
        id2 = uuid.uuid4()
        self.author = Author.objects.create(id=id1, username="John", displayName="John Doe",
                                            url=f"http://localhost:8000/author/{id1}", host="http://localhost:8000/",)
        self.author2 = Author.objects.create(id=id2, username="Jane", displayName="Jane Doe",
                                             url=f"http://localhost:8000/author/{id2}", host="http://localhost:8000/",)

        self.following = Following.objects.create(
            author=self.author, following_author=self.author2, areFriends=False)

    def test_api_authors(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'authors')
        self.assertEqual(len(data['items']), 2)
        self.assertEqual(data['items'][0]['displayName'], 'John Doe')

    def test_api_author_get(self):
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['displayName'], 'John Doe')

    def test_api_author_put(self):
        updated_data = {
            'displayName': 'Jane Smith',
        }
        response = self.client.put(f'/api/authors/{self.author.id}/', data=json.dumps(
            updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['displayName'], 'Jane Smith')

    def test_api_followers(self):
        response = self.client.get(f'/api/authors/{self.author.id}/followers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'followers')
        self.assertEqual(len(data['items']), 1)

    def test_api_follower_make_friends(self):

        url = reverse('author_make_friends', args=[
                      str(self.author.id), self.author2.url])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        response = self.client.get(f'/api/authors/{self.author2.id}/followers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'followers')
        self.assertEqual(len(data['items']), 1)

    def test_api_follower_delete(self):
        url = reverse('authors', args=[str(self.author.id), self.author2.url])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        response = self.client.get(f'/api/authors/{self.author2.id}/followers')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['type'], 'followers')
        self.assertEqual(len(data['items']), 0)
