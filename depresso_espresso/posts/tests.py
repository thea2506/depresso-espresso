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
      response = self.client.post(reverse('make_post'), {
        'title': 'Test Post',
        'visibility': 'PUBLIC',
        'description': 'This is a test post',
        'contentType': 'text/plain',
        'content': 'Hello, world!'
      })
      self.assertEqual(response.status_code, 200)
      self.assertTrue('success' in response.json())
      self.assertTrue('id' in response.json())

    def test_get_all_posts(self):
        response = self.client.get(reverse('get_all_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts' in response.json())
        self.assertTrue('authors' in response.json())

    def test_get_author_posts(self):
        response = self.client.get(reverse('get_author_posts', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts' in response.json())
        self.assertTrue('authors' in response.json())

    def test_get_post_comments(self):
        post = Post.objects.create(title='Test Post', visibility='PUBLIC', description='This is a test post', contentType='text/plain', content='Hello, world!', author=self.user)
        response = self.client.post(reverse('make_comment'), {
          'comment': 'This is a test comment',
          'contenttype': 'text/plain',
          'author': self.user.id,
          'postid': post.id,
          'visibility': 'PUBLIC',
          'published': '2021-04-20T00:00:00Z',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue('success' in response.json())
        
        response = self.client.get(reverse('get_post_comments', args=[self.user.id, post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('author' in response.json()[0])
        self.assertTrue('comment' in response.json()[0])
        self.assertTrue('contentType' in response.json()[0])
        self.assertTrue('published' in response.json()[0])
        self.assertTrue('id' in response.json()[0])


    def test_like_post(self):
        post = Post.objects.create(title='Test Post', visibility='PUBLIC', description='This is a test post', contentType='text/plain', content='Hello, world!', author=self.user)
        response = self.client.post(reverse('like_post', args=[self.user.id, post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('already_liked' in response.json())

    def test_like_comment(self):
        post = Post.objects.create(title='Test Post', visibility='PUBLIC', description='This is a test post', contentType='text/plain', content='Hello, world!', author=self.user)
        comment = Comment.objects.create(comment='Test Comment', author=self.user, postid=post, visibility='PUBLIC', contenttype='text/plain', likecount=0, publishdate='2021-04-20T00:00:00Z')
        response = self.client.post(reverse('like_comment', args=[self.user.id, post.id, comment.id]))
        self.assertEqual(response.status_code, 200)
        
        comment_from_db = Comment.objects.get(id=comment.id)
        self.assertEqual(comment_from_db.comment, 'Test Comment')
        self.assertEqual(comment_from_db.likecount, 1)



    def test_delete_post(self):
        post = Post.objects.create(title='Test Post', visibility='PUBLIC', description='This is a test post', contentType='text/plain', content='Hello, world!', author=self.user)
        response = self.client.post(reverse('delete_post'), {
            'postid': post.id
        })
        self.assertEqual(response.status_code, 200)
        
        post_from_db = Post.objects.get(id=post.id)
        self.assertIsNone(post_from_db)
        


if __name__ == '__main__':
    unittest.main()