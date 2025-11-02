"""
Unit Tests for Shopping Cart System
====================================

Comprehensive test suite for the shopping cart system.

Author: Mohamed Izzath
Date: November 2, 2025

Run with: python -m pytest test_shopping_cart.py -v
Or simply: python test_shopping_cart.py
"""

import unittest
from shopping_cart import (
    Book, MusicAlbum, SoftwareLicense, ShoppingCart,
    analyze_product_sequences
)


class TestBook(unittest.TestCase):
    """Test cases for the Book class."""
    
    def test_create_book(self):
        """Test creating a book with valid parameters."""
        book = Book("B001", "Test Book", "Test Author", 300, 25.99, 0.5)
        self.assertEqual(book.product_id, "B001")
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.num_pages, 300)
        self.assertEqual(book.price, 25.99)
        self.assertEqual(book.get_weight(), 0.5)
    
    def test_book_negative_price(self):
        """Test that negative price raises ValueError."""
        with self.assertRaises(ValueError):
            Book("B001", "Test", "Author", 300, -10.0, 0.5)
    
    def test_book_negative_pages(self):
        """Test that negative pages raises ValueError."""
        with self.assertRaises(ValueError):
            Book("B001", "Test", "Author", -100, 10.0, 0.5)
    
    def test_book_zero_pages(self):
        """Test that zero pages raises ValueError."""
        with self.assertRaises(ValueError):
            Book("B001", "Test", "Author", 0, 10.0, 0.5)
    
    def test_book_negative_weight(self):
        """Test that negative weight raises ValueError."""
        with self.assertRaises(ValueError):
            Book("B001", "Test", "Author", 100, 10.0, -0.5)
    
    def test_book_description(self):
        """Test book description format."""
        book = Book("B001", "Test Book", "Author", 300, 25.99, 0.5)
        desc = book.get_description()
        self.assertIn("Test Book", desc)
        self.assertIn("Author", desc)
        self.assertIn("300", desc)


class TestMusicAlbum(unittest.TestCase):
    """Test cases for the MusicAlbum class."""
    
    def test_create_album(self):
        """Test creating an album with valid parameters."""
        album = MusicAlbum("M001", "Artist", "Album", 12, 14.99, 0.1)
        self.assertEqual(album.product_id, "M001")
        self.assertEqual(album.artist, "Artist")
        self.assertEqual(album.title, "Album")
        self.assertEqual(album.num_tracks, 12)
        self.assertEqual(album.price, 14.99)
        self.assertEqual(album.get_weight(), 0.1)
    
    def test_album_negative_tracks(self):
        """Test that negative tracks raises ValueError."""
        with self.assertRaises(ValueError):
            MusicAlbum("M001", "Artist", "Album", -5, 14.99, 0.1)
    
    def test_album_zero_tracks(self):
        """Test that zero tracks raises ValueError."""
        with self.assertRaises(ValueError):
            MusicAlbum("M001", "Artist", "Album", 0, 14.99, 0.1)
    
    def test_album_description(self):
        """Test album description format."""
        album = MusicAlbum("M001", "Artist", "Album", 12, 14.99, 0.1)
        desc = album.get_description()
        self.assertIn("Artist", desc)
        self.assertIn("Album", desc)
        self.assertIn("12", desc)


class TestSoftwareLicense(unittest.TestCase):
    """Test cases for the SoftwareLicense class."""
    
    def test_create_software(self):
        """Test creating a software license with valid parameters."""
        software = SoftwareLicense("S001", "Test Software", 99.99)
        self.assertEqual(software.product_id, "S001")
        self.assertEqual(software.software_name, "Test Software")
        self.assertEqual(software.price, 99.99)
    
    def test_software_zero_weight(self):
        """Test that software has zero weight (digital product)."""
        software = SoftwareLicense("S001", "Test Software", 99.99)
        self.assertEqual(software.get_weight(), 0.0)
    
    def test_software_description(self):
        """Test software description format."""
        software = SoftwareLicense("S001", "Test Software", 99.99)
        desc = software.get_description()
        self.assertIn("Test Software", desc)
        self.assertIn("Digital", desc)


class TestShoppingCart(unittest.TestCase):
    """Test cases for the ShoppingCart class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cart = ShoppingCart()
        self.book = Book("B001", "Test Book", "Author", 300, 25.99, 0.5)
        self.album = MusicAlbum("M001", "Artist", "Album", 12, 14.99, 0.1)
        self.software = SoftwareLicense("S001", "Software", 99.99)
    
    def test_empty_cart(self):
        """Test that new cart is empty."""
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_item_count(), 0)
        self.assertEqual(self.cart.get_total_price(), 0.0)
        self.assertEqual(self.cart.get_total_weight(), 0.0)
    
    def test_add_product(self):
        """Test adding a product to cart."""
        self.cart.add_product(self.book)
        self.assertFalse(self.cart.is_empty())
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_add_multiple_products(self):
        """Test adding multiple products."""
        self.cart.add_product(self.book)
        self.cart.add_product(self.album)
        self.cart.add_product(self.software)
        self.assertEqual(self.cart.get_item_count(), 3)
    
    def test_total_price(self):
        """Test calculating total price."""
        self.cart.add_product(self.book)    # 25.99
        self.cart.add_product(self.album)   # 14.99
        self.cart.add_product(self.software)  # 99.99
        expected = 25.99 + 14.99 + 99.99
        self.assertAlmostEqual(self.cart.get_total_price(), expected, places=2)
    
    def test_total_weight(self):
        """Test calculating total weight."""
        self.cart.add_product(self.book)    # 0.5 kg
        self.cart.add_product(self.album)   # 0.1 kg
        self.cart.add_product(self.software)  # 0.0 kg (digital)
        expected = 0.5 + 0.1 + 0.0
        self.assertAlmostEqual(self.cart.get_total_weight(),
                               expected, places=2)
    
    def test_remove_product(self):
        """Test removing a product by ID."""
        self.cart.add_product(self.book)
        self.cart.add_product(self.album)
        
        result = self.cart.remove_product("B001")
        self.assertTrue(result)
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_remove_nonexistent_product(self):
        """Test removing a product that doesn't exist."""
        self.cart.add_product(self.book)
        result = self.cart.remove_product("NONEXISTENT")
        self.assertFalse(result)
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_remove_from_empty_cart(self):
        """Test removing from an empty cart."""
        result = self.cart.remove_product("B001")
        self.assertFalse(result)
    
    def test_remove_all_products(self):
        """Test removing all instances of a product."""
        self.cart.add_product(self.book)
        self.cart.add_product(self.book)
        self.cart.add_product(self.book)
        self.cart.add_product(self.album)
        
        count = self.cart.remove_all_products("B001")
        self.assertEqual(count, 3)
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_clear_cart(self):
        """Test clearing all items from cart."""
        self.cart.add_product(self.book)
        self.cart.add_product(self.album)
        self.cart.add_product(self.software)
        
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())
        self.assertEqual(self.cart.get_item_count(), 0)
    
    def test_get_items_returns_copy(self):
        """Test that get_items returns a copy, not the original list."""
        self.cart.add_product(self.book)
        items = self.cart.get_items()
        items.clear()  # Modify the returned list
        
        # Original cart should still have the item
        self.assertEqual(self.cart.get_item_count(), 1)
    
    def test_product_sequence(self):
        """Test getting the product sequence."""
        self.cart.add_product(self.book)
        self.cart.add_product(self.album)
        self.cart.add_product(self.software)
        
        sequence = self.cart.get_product_sequence()
        self.assertEqual(sequence, ["B001", "M001", "S001"])
    
    def test_add_invalid_type(self):
        """Test that adding non-Product raises TypeError."""
        with self.assertRaises(TypeError):
            self.cart.add_product("not a product")
    
    def test_add_duplicate_products(self):
        """Test adding the same product multiple times."""
        self.cart.add_product(self.book)
        self.cart.add_product(self.book)
        self.cart.add_product(self.book)
        
        self.assertEqual(self.cart.get_item_count(), 3)
        # Price should be 3x the book price
        expected_price = 3 * self.book.price
        self.assertAlmostEqual(
            self.cart.get_total_price(), 
            expected_price, 
            places=2
        )


class TestProductSequenceAnalysis(unittest.TestCase):
    """Test cases for the recommendation system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.book_a = Book("A", "Book A", "Author", 300, 20.0, 0.5)
        self.book_b = Book("B", "Book B", "Author", 300, 20.0, 0.5)
        self.book_c = Book("C", "Book C", "Author", 300, 20.0, 0.5)
    
    def test_empty_carts(self):
        """Test analysis with empty carts."""
        carts = [ShoppingCart(), ShoppingCart()]
        stats = analyze_product_sequences(carts)
        self.assertEqual(len(stats), 0)
    
    def test_single_product_carts(self):
        """Test carts with only one product each."""
        cart1 = ShoppingCart()
        cart1.add_product(self.book_a)
        
        cart2 = ShoppingCart()
        cart2.add_product(self.book_b)
        
        stats = analyze_product_sequences([cart1, cart2])
        # No predecessors since each cart has only one item
        self.assertEqual(len(stats), 0)
    
    def test_simple_sequence(self):
        """Test simple A -> B sequence."""
        cart1 = ShoppingCart()
        cart1.add_product(self.book_a)
        cart1.add_product(self.book_b)
        
        cart2 = ShoppingCart()
        cart2.add_product(self.book_a)
        cart2.add_product(self.book_b)
        
        stats = analyze_product_sequences([cart1, cart2])
        
        # B should have A as predecessor, appearing 2 times
        self.assertIn("B", stats)
        self.assertEqual(stats["B"].most_common_predecessor, "A")
        self.assertEqual(stats["B"].occurrences, 2)
    
    def test_complex_sequence(self):
        """Test the example from the assignment."""
        # Cart 1: A -> B
        cart1 = ShoppingCart()
        cart1.add_product(self.book_a)
        cart1.add_product(self.book_b)
        
        # Cart 2: A -> B
        cart2 = ShoppingCart()
        cart2.add_product(self.book_a)
        cart2.add_product(self.book_b)
        
        # Cart 3: A -> C
        cart3 = ShoppingCart()
        cart3.add_product(self.book_a)
        cart3.add_product(self.book_c)
        
        # Cart 4: C -> B
        cart4 = ShoppingCart()
        cart4.add_product(self.book_c)
        cart4.add_product(self.book_b)
        
        stats = analyze_product_sequences([cart1, cart2, cart3, cart4])
        
        # B is added after A: 2 times (most common)
        # B is added after C: 1 time
        self.assertEqual(stats["B"].most_common_predecessor, "A")
        self.assertEqual(stats["B"].occurrences, 2)
        
        # C is added after A: 1 time
        self.assertEqual(stats["C"].most_common_predecessor, "A")
        self.assertEqual(stats["C"].occurrences, 1)
    
    def test_multiple_products_in_sequence(self):
        """Test cart with multiple products."""
        cart = ShoppingCart()
        cart.add_product(self.book_a)
        cart.add_product(self.book_b)
        cart.add_product(self.book_c)
        
        stats = analyze_product_sequences([cart])
        
        # B comes after A
        self.assertEqual(stats["B"].most_common_predecessor, "A")
        self.assertEqual(stats["B"].occurrences, 1)
        
        # C comes after B
        self.assertEqual(stats["C"].most_common_predecessor, "B")
        self.assertEqual(stats["C"].occurrences, 1)


class TestProductRepresentations(unittest.TestCase):
    """Test string representations of products."""
    
    def test_book_str(self):
        """Test book __str__ method."""
        book = Book("B001", "Test", "Author", 100, 10.0, 0.5)
        s = str(book)
        self.assertIsInstance(s, str)
        self.assertTrue(len(s) > 0)
    
    def test_book_repr(self):
        """Test book __repr__ method."""
        book = Book("B001", "Test", "Author", 100, 10.0, 0.5)
        r = repr(book)
        self.assertIn("Book", r)
        self.assertIn("B001", r)
    
    def test_cart_str_empty(self):
        """Test cart __str__ when empty."""
        cart = ShoppingCart()
        s = str(cart)
        self.assertIn("Empty", s)
    
    def test_cart_str_with_items(self):
        """Test cart __str__ with items."""
        cart = ShoppingCart()
        cart.add_product(Book("B001", "Test", "Author", 100, 10.0, 0.5))
        s = str(cart)
        self.assertIn("Test", s)
        self.assertIn("10.00", s)


def run_tests():
    """Run all tests with detailed output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBook))
    suite.addTests(loader.loadTestsFromTestCase(TestMusicAlbum))
    suite.addTests(loader.loadTestsFromTestCase(TestSoftwareLicense))
    suite.addTests(loader.loadTestsFromTestCase(TestShoppingCart))
    suite.addTests(loader.loadTestsFromTestCase(TestProductSequenceAnalysis))
    suite.addTests(loader.loadTestsFromTestCase(TestProductRepresentations))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
