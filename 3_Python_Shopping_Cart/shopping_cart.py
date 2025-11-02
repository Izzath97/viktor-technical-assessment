"""
Shopping Cart System
====================

A flexible, object-oriented shopping cart system supporting multiple product types.

Author: Mohamed Izzath
Date: November 2, 2025

This module implements a shopping cart for an online store selling:
- Books
- Music Albums (CDs)
- Software Licenses

Features:
---------
- Add/remove products from cart
- Calculate total price
- Calculate total weight
- Product sequence analysis for recommendations
- Extensible design for future product types

Design Principles:
------------------
- SOLID principles
- Clean code practices
- Type hints for clarity
- Comprehensive documentation
- Easy to extend and maintain
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict, Counter


# ============================================================================
# ABSTRACT BASE CLASS FOR PRODUCTS
# ============================================================================

class Product(ABC):
    """
    Abstract base class for all products in the store.
    
    This class defines the common interface that all products must implement.
    Using inheritance and polymorphism allows for easy addition of new product
    types without modifying existing code.
    
    Attributes:
        product_id (str): Unique identifier for the product
        price (float): Price in euros
    """
    
    def __init__(self, product_id: str, price: float):
        """
        Initialize a product.
        
        Args:
            product_id: Unique identifier for the product
            price: Price in euros (must be non-negative)
            
        Raises:
            ValueError: If price is negative
        """
        if price < 0:
            raise ValueError("Price cannot be negative")
        
        self._product_id = product_id
        self._price = price
    
    @property
    def product_id(self) -> str:
        """Get the product ID."""
        return self._product_id
    
    @property
    def price(self) -> float:
        """Get the product price in euros."""
        return self._price
    
    @abstractmethod
    def get_weight(self) -> float:
        """
        Get the weight of the product in kilograms.
        
        Returns:
            Weight in kg (0 for digital products)
        """
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a human-readable description of the product.
        
        Returns:
            String description of the product
        """
        pass
    
    def __str__(self) -> str:
        """String representation of the product."""
        return self.get_description()
    
    def __repr__(self) -> str:
        """Developer-friendly representation of the product."""
        return f"{self.__class__.__name__}(id={self.product_id}, price={self.price}€)"


# ============================================================================
# CONCRETE PRODUCT CLASSES
# ============================================================================

class Book(Product):
    """
    Represents a physical book product.
    
    Attributes:
        product_id (str): Unique identifier
        title (str): Book title
        author (str): Book author
        num_pages (int): Number of pages
        price (float): Price in euros
        weight (float): Weight in kilograms
    """
    
    def __init__(
        self,
        product_id: str,
        title: str,
        author: str,
        num_pages: int,
        price: float,
        weight: float
    ):
        """
        Initialize a Book.
        
        Args:
            product_id: Unique identifier
            title: Book title
            author: Book author
            num_pages: Number of pages (must be positive)
            price: Price in euros
            weight: Weight in kilograms (must be non-negative)
            
        Raises:
            ValueError: If num_pages is not positive or weight is negative
        """
        super().__init__(product_id, price)
        
        if num_pages <= 0:
            raise ValueError("Number of pages must be positive")
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        
        self.title = title
        self.author = author
        self.num_pages = num_pages
        self._weight = weight
    
    def get_weight(self) -> float:
        """Get the weight of the book in kilograms."""
        return self._weight
    
    def get_description(self) -> str:
        """Get a description of the book."""
        return (f"Book: '{self.title}' by {self.author} "
                f"({self.num_pages} pages, {self._weight}kg, €{self.price})")


class MusicAlbum(Product):
    """
    Represents a physical music album (CD).
    
    Attributes:
        product_id (str): Unique identifier
        artist (str): Artist/band name
        title (str): Album title
        num_tracks (int): Number of tracks
        price (float): Price in euros
        weight (float): Weight in kilograms
    """
    
    def __init__(
        self,
        product_id: str,
        artist: str,
        title: str,
        num_tracks: int,
        price: float,
        weight: float
    ):
        """
        Initialize a Music Album.
        
        Args:
            product_id: Unique identifier
            artist: Artist/band name
            title: Album title
            num_tracks: Number of tracks (must be positive)
            price: Price in euros
            weight: Weight in kilograms (must be non-negative)
            
        Raises:
            ValueError: If num_tracks is not positive or weight is negative
        """
        super().__init__(product_id, price)
        
        if num_tracks <= 0:
            raise ValueError("Number of tracks must be positive")
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        
        self.artist = artist
        self.title = title
        self.num_tracks = num_tracks
        self._weight = weight
    
    def get_weight(self) -> float:
        """Get the weight of the album in kilograms."""
        return self._weight
    
    def get_description(self) -> str:
        """Get a description of the album."""
        return (f"Album: '{self.title}' by {self.artist} "
                f"({self.num_tracks} tracks, {self._weight}kg, €{self.price})")


class SoftwareLicense(Product):
    """
    Represents a digital software license.
    
    Digital products have no physical weight.
    
    Attributes:
        product_id (str): Unique identifier
        software_name (str): Name of the software
        price (float): Price in euros
    """
    
    def __init__(
        self,
        product_id: str,
        software_name: str,
        price: float
    ):
        """
        Initialize a Software License.
        
        Args:
            product_id: Unique identifier
            software_name: Name of the software
            price: Price in euros
        """
        super().__init__(product_id, price)
        self.software_name = software_name
    
    def get_weight(self) -> float:
        """Get the weight of the software license (always 0 - digital product)."""
        return 0.0
    
    def get_description(self) -> str:
        """Get a description of the software license."""
        return f"Software License: {self.software_name} (Digital, €{self.price})"


# ============================================================================
# SHOPPING CART CLASS
# ============================================================================

class ShoppingCart:
    """
    Shopping cart that holds products and calculates totals.
    
    The cart maintains the order in which products are added for the
    recommendation system. Products can be added multiple times.
    
    Attributes:
        items (List[Product]): List of products in the cart (maintains order)
    """
    
    def __init__(self):
        """Initialize an empty shopping cart."""
        self._items: List[Product] = []
    
    def add_product(self, product: Product) -> None:
        """
        Add a product to the shopping cart.
        
        Args:
            product: The product to add
            
        Raises:
            TypeError: If product is not a Product instance
        """
        if not isinstance(product, Product):
            raise TypeError("Can only add Product instances to cart")
        
        self._items.append(product)
    
    def remove_product(self, product_id: str) -> bool:
        """
        Remove the first occurrence of a product with the given ID from the cart.
        
        Args:
            product_id: The ID of the product to remove
            
        Returns:
            True if product was removed, False if not found
        """
        for i, item in enumerate(self._items):
            if item.product_id == product_id:
                self._items.pop(i)
                return True
        return False
    
    def remove_all_products(self, product_id: str) -> int:
        """
        Remove all occurrences of a product with the given ID from the cart.
        
        Args:
            product_id: The ID of the product to remove
            
        Returns:
            Number of items removed
        """
        original_length = len(self._items)
        self._items = [item for item in self._items if item.product_id != product_id]
        return original_length - len(self._items)
    
    def clear(self) -> None:
        """Remove all items from the cart."""
        self._items.clear()
    
    def get_total_price(self) -> float:
        """
        Calculate the total price of all items in the cart.
        
        Returns:
            Total price in euros
        """
        return sum(item.price for item in self._items)
    
    def get_total_weight(self) -> float:
        """
        Calculate the total weight of all items in the cart.
        
        Digital products (like software licenses) have zero weight.
        
        Returns:
            Total weight in kilograms
        """
        return sum(item.get_weight() for item in self._items)
    
    def get_item_count(self) -> int:
        """
        Get the number of items in the cart.
        
        Returns:
            Number of items
        """
        return len(self._items)
    
    def get_items(self) -> List[Product]:
        """
        Get a copy of all items in the cart.
        
        Returns:
            List of products (copy to prevent external modification)
        """
        return self._items.copy()
    
    def is_empty(self) -> bool:
        """
        Check if the cart is empty.
        
        Returns:
            True if cart is empty, False otherwise
        """
        return len(self._items) == 0
    
    def get_product_sequence(self) -> List[str]:
        """
        Get the sequence of product IDs in the order they were added.
        
        This is useful for the recommendation system to analyze
        which products are typically added together.
        
        Returns:
            List of product IDs in order of addition
        """
        return [item.product_id for item in self._items]
    
    def __str__(self) -> str:
        """String representation of the cart."""
        if self.is_empty():
            return "Shopping Cart: Empty"
        
        items_str = "\n".join(f"  - {item.get_description()}" for item in self._items)
        return (f"Shopping Cart ({self.get_item_count()} items):\n{items_str}\n"
                f"Total: €{self.get_total_price():.2f}, "
                f"Weight: {self.get_total_weight():.2f}kg")
    
    def __repr__(self) -> str:
        """Developer-friendly representation of the cart."""
        return f"ShoppingCart(items={self.get_item_count()}, total=€{self.get_total_price():.2f})"


# ============================================================================
# RECOMMENDATION SYSTEM
# ============================================================================

@dataclass
class ProductSequenceStats:
    """
    Statistics about product addition sequences.
    
    Attributes:
        product_id: The product ID
        most_common_predecessor: ID of the product most often added before this one
        occurrences: Number of times this sequence occurs
    """
    product_id: str
    most_common_predecessor: Optional[str]
    occurrences: int


def analyze_product_sequences(carts: List[ShoppingCart]) -> Dict[str, ProductSequenceStats]:
    """
    Analyze product addition sequences across multiple shopping carts.
    
    For each product, determines which product is most commonly added
    immediately before it. This helps build a recommendation system
    that can suggest "customers who added X also added Y".
    
    Args:
        carts: List of shopping carts to analyze
        
    Returns:
        Dictionary mapping product IDs to their sequence statistics
        
    Example:
        >>> cart1 = ShoppingCart()
        >>> cart1.add_product(book_a)  # A
        >>> cart1.add_product(book_b)  # B (after A)
        >>>
        >>> cart2 = ShoppingCart()
        >>> cart2.add_product(book_a)  # A
        >>> cart2.add_product(book_b)  # B (after A)
        >>>
        >>> cart3 = ShoppingCart()
        >>> cart3.add_product(book_a)  # A
        >>> cart3.add_product(album_c) # C (after A)
        >>> cart3.add_product(book_b)  # B (after C)
        >>>
        >>> stats = analyze_product_sequences([cart1, cart2, cart3])
        >>> # B is added after A: 2 times
        >>> # B is added after C: 1 time
        >>> # So B's most common predecessor is A with 2 occurrences
    """
    # Track what product comes after which product
    # Structure: {product_id: {predecessor_id: count}}
    predecessor_counts: Dict[str, Counter] = defaultdict(Counter)
    
    # Analyze each cart
    for cart in carts:
        sequence = cart.get_product_sequence()
        
        # Look at each pair of consecutive products
        for i in range(1, len(sequence)):
            predecessor = sequence[i - 1]
            current = sequence[i]
            predecessor_counts[current][predecessor] += 1
    
    # Build statistics for each product
    results: Dict[str, ProductSequenceStats] = {}
    
    for product_id, predecessors in predecessor_counts.items():
        if predecessors:
            # Find the most common predecessor
            most_common = predecessors.most_common(1)[0]
            most_common_pred_id, count = most_common
            
            results[product_id] = ProductSequenceStats(
                product_id=product_id,
                most_common_predecessor=most_common_pred_id,
                occurrences=count
            )
        else:
            # Product has no predecessors (always added first)
            results[product_id] = ProductSequenceStats(
                product_id=product_id,
                most_common_predecessor=None,
                occurrences=0
            )
    
    return results


def print_sequence_analysis(
    stats: Dict[str, ProductSequenceStats],
    product_names: Optional[Dict[str, str]] = None
) -> None:
    """
    Print a human-readable report of product sequence analysis.
    
    Args:
        stats: Product sequence statistics from analyze_product_sequences()
        product_names: Optional mapping of product IDs to human-readable names
    """
    if not stats:
        print("No sequence data available.")
        return
    
    print("\n" + "="*70)
    print("PRODUCT SEQUENCE ANALYSIS - RECOMMENDATION INSIGHTS")
    print("="*70)
    print("\nThis shows which product is most commonly added BEFORE each product.")
    print("Use this data to recommend products based on cart sequence patterns.\n")
    
    # Sort by occurrences (descending) for more interesting insights first
    sorted_stats = sorted(
        stats.items(),
        key=lambda x: x[1].occurrences,
        reverse=True
    )
    
    for product_id, stat in sorted_stats:
        product_name = product_names.get(product_id, product_id) if product_names else product_id
        
        if stat.most_common_predecessor is None:
            print(f"📦 {product_name}")
            print(f"   └─ Often added first (no clear predecessor pattern)")
        else:
            pred_name = (product_names.get(stat.most_common_predecessor, stat.most_common_predecessor)
                        if product_names else stat.most_common_predecessor)
            print(f"📦 {product_name}")
            print(f"   └─ Most often added AFTER: {pred_name}")
            print(f"   └─ Occurrences: {stat.occurrences} time(s)")
        print()
    
    print("="*70)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("Shopping Cart System - Demo\n")
    print("="*70)
    
    # Create some products
    book1 = Book(
        product_id="B001",
        title="Clean Code",
        author="Robert C. Martin",
        num_pages=464,
        price=34.99,
        weight=0.7
    )
    
    book2 = Book(
        product_id="B002",
        title="Design Patterns",
        author="Gang of Four",
        num_pages=395,
        price=44.99,
        weight=0.8
    )
    
    album1 = MusicAlbum(
        product_id="M001",
        artist="The Beatles",
        title="Abbey Road",
        num_tracks=17,
        price=15.99,
        weight=0.1
    )
    
    software1 = SoftwareLicense(
        product_id="S001",
        software_name="PyCharm Professional",
        price=199.00
    )
    
    # Create a shopping cart
    cart = ShoppingCart()
    
    print("\n1. Adding products to cart...")
    cart.add_product(book1)
    cart.add_product(album1)
    cart.add_product(software1)
    cart.add_product(book2)
    
    print(cart)
    
    print("\n2. Cart Statistics:")
    print(f"   Total Items: {cart.get_item_count()}")
    print(f"   Total Price: €{cart.get_total_price():.2f}")
    print(f"   Total Weight: {cart.get_total_weight():.2f}kg")
    
    print("\n3. Removing a product...")
    cart.remove_product("M001")
    print(f"   After removing album: €{cart.get_total_price():.2f}, "
          f"{cart.get_total_weight():.2f}kg")
    
    print("\n" + "="*70)
    print("\nShoppingCart System ready to use!")

