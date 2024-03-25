import json
import uuid
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Author
from posts.models import Post
from .views import handle_inbox

class InboxTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(
            host="example.com",
            displayName="John Doe",
            url="http://example.com/authors/johndoe",
            username="johndoe",
            isExternalAuthor=False,
            id=uuid.uuid4(),
            type="author",
        )
        self.post = Post.objects.create(
            title="Test Post",
            id=uuid.uuid4(),
            origin="http://example.com",
            description="This is a test post",
            visibility="PUBLIC",
            contentType="text/plain",
            content="Hello, world!",
            author=self.author
        )

    def test_handle_inbox_get(self):
        url = reverse('handle_inbox', args=[self.author.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['type'], 'inbox')
        self.assertEqual(str(data['author']), str(self.author.id))
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['model'], 'posts.post')
        self.assertEqual(data['items'][0]['fields']['title'], self.post.title)

