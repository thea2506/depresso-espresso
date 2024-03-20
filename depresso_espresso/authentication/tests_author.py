from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Author, Following
import uuid

class HandleFollowTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(
            id=uuid.uuid4(),
            type="author",
            url="http://localhost:8000/author/1",
            host="http://localhost:8000/",
            displayName="Author 1",
            username="author1",
            github="author1",
            profileImage="http://localhost:8000/media/profile.jpg"
        )
        self.author2 = Author.objects.create(
            id=uuid.uuid4(),
            type="author",
            url="http://localhost:8000/author/2",
            host="http://localhost:8000/",
            displayName="Author 2",
            username="author2",
            github="author2",
            profileImage="http://localhost:8000/media/profile.jpg"
        )
        self.following = Following.objects.create(
            authorid=self.author2.id,
            followingid=self.author1.id,
            areFriends=False
        )
        

    def test_get_followers(self):
        url = reverse('handle_follow', args=[self.author1.id, self.author2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['type'], 'followers')
        self.assertEqual(len(response.json()['items']), 2)

    def test_get_followers_not_found(self):
        url = reverse('handle_follow', args=[self.author2.id, self.author1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['message'], 'Author not found')

    def test_remove_follower(self):
        url = reverse('handle_follow', args=[self.author1.id, self.author2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(Following.objects.filter(authorid=2, followingid=1).exists(), False)
