# import json
# from django.test import TestCase
# from django.urls import reverse
# from .models import Author

# class RegisterTestCase(TestCase):
#   def test_register_success(self):
#     response = self.client.post(reverse('signup'), {'username': 'testuser', 'password': 'testpassword'})
#     self.assertEqual(response.status_code, 302)
#     if response.content:
#       data = json.loads(response.content)
#       self.assertTrue(data['success'])
  
#   def test_register_failure(self):
#     response = self.client.post(reverse('signup'), {'username': 'testuser'})
#     self.assertEqual(response.status_code, 302)
#     if response.content:
#       data = json.loads(response.content)
#       self.assertFalse(data['success'])

# class LoginUserTestCase(TestCase):
#     def test_login_success(self):
#         response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'testpassword'})
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content)
#         print("this is data", data)
#         self.assertTrue(data['success'])
#         self.assertIsNotNone(data['id'])
    
#     def test_login_failure(self):
#         response = self.client.post(reverse('signin'), {'username': 'testuser', 'password': 'wrongpassword'})
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content)
#         self.assertFalse(data['success'])

# class LogoutUserTestCase(TestCase):
#     def test_logout(self):
#         response = self.client.post(reverse('logoutUser'))
#         self.assertEqual(response.status_code, 302)
#         data = json.loads(response.content)
#         self.assertTrue(data['success'])

# class CurUserTestCase(TestCase):
#     def test_cur_user_success(self):
#         user = Author.objects.create(username='testuser', password='testpassword')
#         session = self.client.session
#         session['_auth_user_id'] = user.id
#         session.save()
#         response = self.client.get(reverse('curUser'))
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content)
#         self.assertTrue(data['success'])
#         self.assertEqual(data['id'], user.id)
#         self.assertEqual(data['username'], user.username)
    
#     def test_cur_user_failure(self):
#         response = self.client.get(reverse('curUser'))
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.content)
#         self.assertFalse(data['success'])