from django.test import TestCase, Client
from django.urls import reverse
from books.models import Books
from booklibrary.models import UserBook
from homepage.models import CustomUser as User

class LibraryViewTests(TestCase):

    def setUp(self):
        # Setting up a test client
        self.client = Client()

        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Create a sample book
        self.book = Books.objects.create(title="Test Book", author="Test Author")

    def test_show_library(self):
        response = self.client.get(reverse('booklibrary:show_library'))
        self.assertEqual(response.status_code, 200)

    def test_load_books_ajax(self):
        response = self.client.post(reverse('booklibrary:load_books'), {'search_query': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Book', str(response.content))

    def test_get_user_bookshelf(self):
        # You have to log in first to access this view
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('booklibrary:get_user_bookshelf'))
        self.assertEqual(response.status_code, 200)

    def test_borrow_book(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('booklibrary:borrow_book'), {'book_id': self.book.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book added to shelf successfully!', str(response.content))

    def test_complete_reading(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Borrow the book first
        UserBook.objects.create(user=self.user, book=self.book, status='reading')

        response = self.client.post(reverse('booklibrary:complete_reading'), {'book_id': self.book.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Status updated successfully!', str(response.content))

    def test_re_read_book(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Mark the book as completed first
        UserBook.objects.create(user=self.user, book=self.book, status='completed')

        response = self.client.post(reverse('booklibrary:re_read_book'), {'book_id': self.book.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book status updated to currently reading!', str(response.content))
