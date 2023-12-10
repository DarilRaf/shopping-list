from django.test import TestCase, Client
from django.urls import reverse
from homepage.models import CustomUser as User
from booklibrary.models import UserBook
from .models import Bookmark
from books.models import Books

class BookmarkViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')
        # Create a test book
        self.test_book = Books.objects.create(title='Test Book', genre='Fiction')
        # Create a test UserBook
        self.user_book = UserBook.objects.create(user=self.user, book=self.test_book)

    def test_show_bookmark(self):
            self.client.login(username='testuser', password='12345')
            response = self.client.get(reverse('bookmark:show_bookmark'))
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.user_book, response.context['bookmarks'])
    
    def test_add_bookmark(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('bookmark:add_bookmark', args=(self.user_book.id,)))
        bookmark_exists = Bookmark.objects.filter(user=self.user, book=self.user_book).exists()
        self.assertTrue(bookmark_exists)

    def test_delete_bookmark(self):
        bookmark = Bookmark.objects.create(user=self.user, book=self.user_book)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('bookmark:delete_bookmark', args=(bookmark.id,)))
        bookmark_exists = Bookmark.objects.filter(id=bookmark.id).exists()
        self.assertFalse(bookmark_exists)

    def test_show_json(self):
        Bookmark.objects.create(user=self.user, book=self.user_book)
        response = self.client.get(reverse('bookmark:show_json'))
        self.assertEqual(response.status_code, 200)

        # Ensure the serialized structure of the bookmark is present in the response
        expected_content = [
            '"model": "bookmark.bookmark"',
            '"user": 1',
            '"book": 1'
        ]
        for content in expected_content:
            self.assertIn(content, str(response.content))


