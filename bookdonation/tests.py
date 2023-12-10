from django.test import TestCase, Client
from django.urls import reverse
from books.models import Books
from booklibrary.models import UserBook
from .models import data_donasi1
from homepage.models import CustomUser as User

class ProductViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        self.product = data_donasi1.objects.create(
            judul_buku="Test Product",
            total_buku=5,
            user=self.user,
            status="menunggu verifikasi"
        )

    def test_hapus_produk_ajax(self):
        response = self.client.delete(reverse('bookdonation:hapus_produk_ajax', args=[self.product.id]))
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(data_donasi1.DoesNotExist):
            data_donasi1.objects.get(pk=self.product.id)

    def test_add_product_ajax(self):
        data = {
            'judul_buku': 'New Product',
            'total_buku': '10',
            'resi': 'Resi123',
            'status': 'menunggu verifikasi'
        }
        response = self.client.post(reverse('bookdonation:add_product_ajax'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data_donasi1.objects.filter(judul_buku='New Product').exists())

    def test_get_product_json(self):
        response = self.client.get(reverse('bookdonation:get_product_json'))
        self.assertIn(str(self.product.judul_buku), str(response.content))

    def test_tambah_produk(self):
        response = self.client.get(reverse('bookdonation:tambah_produk', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.total_buku, 6)

    def test_kurang_produk(self):
        response = self.client.get(reverse('bookdonation:kurang_produk', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.total_buku, 4)

    def test_ubah_status(self):
        response = self.client.get(reverse('bookdonation:ubah_status', args=[self.product.id]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.status, "Sudah diverifikasi")

    def test_show_json_by_id(self):
        response = self.client.get(reverse('bookdonation:show_json_by_id', args=[self.product.id]))
        self.assertIn(str(self.product.judul_buku), str(response.content))