"""
Comprehensive Tests for Shopping Cart System.
"""
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Book, MusicAlbum, SoftwareLicense, Cart
from .recommendations import (
    analyze_product_sequences,
    get_product_recommendations,
    find_frequently_bought_together
)


class ProductModelTests(TestCase):
    """Tests for Product models."""

    def test_book_creation(self):
        book = Book.objects.create(
            title="Clean Code",
            author="Robert C. Martin",
            number_of_pages=464,
            price=Decimal('42.50'),
            weight=Decimal('0.8')
        )
        self.assertEqual(book.get_weight(), Decimal('0.8'))
        self.assertEqual(str(book), "Clean Code by Robert C. Martin")

    def test_music_album_creation(self):
        album = MusicAlbum.objects.create(
            artist="The Beatles",
            title="Abbey Road",
            number_of_tracks=17,
            price=Decimal('15.99'),
            weight=Decimal('0.1')
        )
        self.assertEqual(album.get_weight(), Decimal('0.1'))
        self.assertEqual(str(album), "Abbey Road by The Beatles")

    def test_software_license_creation(self):
        license = SoftwareLicense.objects.create(
            name="IntelliJ IDEA",
            price=Decimal('199.00'),
            license_key="ABC-123-DEF"
        )
        self.assertEqual(license.get_weight(), Decimal('0.00'))
        self.assertEqual(str(license), "IntelliJ IDEA")


class CartModelTests(TestCase):
    """Tests for Cart model operations."""

    def setUp(self):
        self.cart = Cart.objects.create()
        self.book = Book.objects.create(
            title="Design Patterns",
            author="Gang of Four",
            number_of_pages=395,
            price=Decimal('54.99'),
            weight=Decimal('1.2')
        )
        self.album = MusicAlbum.objects.create(
            artist="Pink Floyd",
            title="Dark Side of the Moon",
            number_of_tracks=10,
            price=Decimal('12.99'),
            weight=Decimal('0.09')
        )

    def test_add_item_to_cart(self):
        self.cart.add_item(self.book, quantity=2)
        self.assertEqual(self.cart.get_items_count(), 2)

    def test_add_multiple_items(self):
        self.cart.add_item(self.book, quantity=1)
        self.cart.add_item(self.album, quantity=3)
        self.assertEqual(self.cart.get_items_count(), 4)

    def test_remove_item_from_cart(self):
        self.cart.add_item(self.book)
        removed = self.cart.remove_item(self.book)
        self.assertTrue(removed)
        self.assertEqual(self.cart.get_items_count(), 0)

    def test_update_item_quantity(self):
        self.cart.add_item(self.book, quantity=1)
        self.cart.update_item_quantity(self.book, 5)
        self.assertEqual(self.cart.get_items_count(), 5)

    def test_clear_cart(self):
        self.cart.add_item(self.book)
        self.cart.add_item(self.album)
        self.cart.clear()
        self.assertEqual(self.cart.get_items_count(), 0)

    def test_calculate_total_price(self):
        self.cart.add_item(self.book, quantity=2)
        self.cart.add_item(self.album, quantity=1)
        expected = (Decimal('54.99') * 2) + Decimal('12.99')
        self.assertEqual(self.cart.get_total_price(), expected)

    def test_calculate_total_weight(self):
        self.cart.add_item(self.book, quantity=2)
        self.cart.add_item(self.album, quantity=1)
        expected = (Decimal('1.2') * 2) + Decimal('0.09')
        self.assertEqual(self.cart.get_total_weight(), expected)


class RecommendationSystemTests(TestCase):
    """Tests for recommendation system."""

    def setUp(self):
        self.book1 = Book.objects.create(
            title="Book 1", author="Author A",
            number_of_pages=300, price=Decimal('30'),
            weight=Decimal('0.5')
        )
        self.book2 = Book.objects.create(
            title="Book 2", author="Author B",
            number_of_pages=400, price=Decimal('40'),
            weight=Decimal('0.6')
        )
        self.book3 = Book.objects.create(
            title="Book 3", author="Author C",
            number_of_pages=500, price=Decimal('50'),
            weight=Decimal('0.7')
        )

    def test_analyze_product_sequences(self):
        # Cart 1: Book1 -> Book2
        cart1 = Cart.objects.create()
        cart1.add_item(self.book1)
        cart1.add_item(self.book2)

        # Cart 2: Book1 -> Book2
        cart2 = Cart.objects.create()
        cart2.add_item(self.book1)
        cart2.add_item(self.book2)

        # Cart 3: Book1 -> Book3
        cart3 = Cart.objects.create()
        cart3.add_item(self.book1)
        cart3.add_item(self.book3)

        carts = [cart1, cart2, cart3]
        sequences = analyze_product_sequences(carts)

        book1_id = str(self.book1.id)
        self.assertIn(book1_id, sequences)
        next_product, count = sequences[book1_id]
        self.assertEqual(next_product, str(self.book2.id))
        self.assertEqual(count, 2)

    def test_get_product_recommendations(self):
        cart1 = Cart.objects.create()
        cart1.add_item(self.book1)
        cart1.add_item(self.book2)

        cart2 = Cart.objects.create()
        cart2.add_item(self.book1)
        cart2.add_item(self.book2)

        carts = [cart1, cart2]
        recommendations = get_product_recommendations(
            str(self.book1.id), carts, limit=5
        )

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations[0][0], str(self.book2.id))
        self.assertEqual(recommendations[0][1], 2)

    def test_frequently_bought_together(self):
        cart1 = Cart.objects.create()
        cart1.add_item(self.book1)
        cart1.add_item(self.book2)

        cart2 = Cart.objects.create()
        cart2.add_item(self.book1)
        cart2.add_item(self.book2)

        carts = [cart1, cart2]
        pairs = find_frequently_bought_together(carts, min_frequency=2)

        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0][1], 2)


class ProductAPITests(APITestCase):
    """Tests for Product API endpoints."""

    def test_create_book(self):
        url = '/api/books/'
        data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'number_of_pages': 200,
            'price': '29.99',
            'weight': '0.5'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)

    def test_list_books(self):
        Book.objects.create(
            title='Book 1', author='Author 1',
            number_of_pages=200, price=Decimal('20'),
            weight=Decimal('0.5')
        )
        url = '/api/books/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_music_album(self):
        url = '/api/music-albums/'
        data = {
            'artist': 'Test Artist',
            'title': 'Test Album',
            'number_of_tracks': 12,
            'price': '14.99',
            'weight': '0.1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_software_license(self):
        url = '/api/software-licenses/'
        data = {
            'name': 'Test Software',
            'price': '99.99'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CartAPITests(APITestCase):
    """Tests for Cart API endpoints."""

    def setUp(self):
        self.book = Book.objects.create(
            title='API Test Book',
            author='Author',
            number_of_pages=300,
            price=Decimal('35.00'),
            weight=Decimal('0.8')
        )

    def test_create_cart(self):
        url = '/api/carts/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_item_to_cart(self):
        cart = Cart.objects.create()
        url = f'/api/carts/{cart.id}/add_item/'
        data = {
            'product_type': 'book',
            'product_id': str(self.book.id),
            'quantity': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items_count'], 2)

    def test_remove_item_from_cart(self):
        cart = Cart.objects.create()
        cart.add_item(self.book)

        url = f'/api/carts/{cart.id}/remove_item/'
        data = {
            'product_type': 'book',
            'product_id': str(self.book.id)
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items_count'], 0)

    def test_update_cart_item(self):
        cart = Cart.objects.create()
        cart.add_item(self.book, quantity=1)

        url = f'/api/carts/{cart.id}/update_item/'
        data = {
            'product_type': 'book',
            'product_id': str(self.book.id),
            'quantity': 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items_count'], 5)

    def test_clear_cart(self):
        cart = Cart.objects.create()
        cart.add_item(self.book)

        url = f'/api/carts/{cart.id}/clear/'
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items_count'], 0)

    def test_analyze_sequences_endpoint(self):
        url = '/api/carts/analyze_sequences/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
