import json
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from .models import Author

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
      self.assertEqual(response.json(), {'errors': [['This field is required.'], ['This field is required.'], ['This field is required.'], ['This field is required.']], 'success': False})

class LoginUserTestCase(TestCase):
    def test_login_success(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)
    
    def test_login_failure(self):
        response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

class LogoutUserTestCase(TestCase):
    def test_logout(self):
        response = self.client.post(reverse('logoutUser'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])