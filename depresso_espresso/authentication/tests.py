import json
import uuid
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from .models import Author
from rest_framework.test import APIClient


class RegisterTestCase(TestCase):
    def test_register_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'displayName': 'testuser',
            'password1': 'thisisatestpassword!@$@%5',
            'password2': 'thisisatestpassword!@$@%5',
            'email': 'test@example.com'
        })

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})

    def test_register_failure(self):
        response = self.client.post(reverse('signup'), {
            'password': 'testpassword',
            'email': 'test@example.com'
        })

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'errors': [['This field is required.'], ['This field is required.'], [
                         'This field is required.'], ['This field is required.']], 'success': False})


class LoginUserTestCase(TestCase):
    def test_login_success(self):
        response = self.client.post(
            reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.client.post(
            reverse('signin'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


class LogoutUserTestCase(TestCase):
    def test_logout(self):
        response = self.client.post(reverse('logoutUser'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])


class CurUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            id=uuid.uuid4(),
            type="author",
            url="http://localhost:8000/author/1",
            host="http://localhost:8000/",
            displayName="Author 1",
            username="author1",
            github="author1",
            profileImage="http://localhost:8000/media/profile.jpg"
        )

        self.client.force_login(user=self.author)

    def test_curUser_with_valid_session(self):
        response = self.client.get(
            reverse('curUser'), session=self.client.session)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'type': self.author.type,
            'id': 'http://testserver/api/authors/' + str(self.author.id),
            'displayName': self.author.displayName,
            'github': self.author.github,
            'host': self.author.host,
            'profileImage': self.author.profileImage,
            'url': self.author.url,
            'success': True
        })

    def test_curUser_with_invalid_session(self):
        self.client.logout()
        response = self.client.get(reverse('curUser'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False})
