"""
Comprehensive Examples for Shopping Cart System
================================================

This file demonstrates all features of the shopping cart system including:
- Creating different types of products
- Managing shopping carts
- Calculating prices and weights
- Analyzing product sequences for recommendations

Author: Mohamed Izzath
Date: November 2, 2025
"""

from shopping_cart import (
    Book, MusicAlbum, SoftwareLicense, ShoppingCart,
    analyze_product_sequences, print_sequence_analysis
)


def example_basic_usage():
    """Demonstrate basic shopping cart functionality."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Shopping Cart Usage")
    print("="*80)
    
    # Create products
    book = Book(
        product_id="B001",
        title="Python Crash Course",
        author="Eric Matthes",
        num_pages=544,
        price=29.99,
        weight=0.9
    )
    
    album = MusicAlbum(
        product_id="M001",
        artist="Daft Punk",
        title="Random Access Memories",
        num_tracks=13,
        price=12.99,
        weight=0.1
    )
    
    software = SoftwareLicense(
        product_id="S001",
        software_name="Visual Studio Code Pro",
        price=0.00  # Free!
    )
    
    # Create and fill cart
    cart = ShoppingCart()
    cart.add_product(book)
    cart.add_product(album)
    cart.add_product(software)
    
    print("\nCart Contents:")
    print(cart)
    
    print(f"\n✅ Total Price: €{cart.get_total_price():.2f}")
    print(f"✅ Total Weight: {cart.get_total_weight():.2f}kg")
    print(f"✅ Item Count: {cart.get_item_count()}")


def example_remove_products():
    """Demonstrate removing products from cart."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Adding and Removing Products")
    print("="*80)
    
    cart = ShoppingCart()
    
    # Add multiple copies of same product
    book1 = Book("B001", "Book 1", "Author 1", 300, 19.99, 0.5)
    book2 = Book("B001", "Book 1", "Author 1", 300, 19.99, 0.5)  # Same ID
    book3 = Book("B002", "Book 2", "Author 2", 250, 24.99, 0.6)
    
    cart.add_product(book1)
    cart.add_product(book2)
    cart.add_product(book3)
    
    print(f"\nInitial cart: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")
    
    # Remove one instance of B001
    removed = cart.remove_product("B001")
    print(f"\nRemoved one B001: {removed}")
    print(f"Cart now: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")
    
    # Remove all instances of B001
    count = cart.remove_all_products("B001")
    print(f"\nRemoved all B001: {count} item(s)")
    print(f"Cart now: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")


def example_mixed_products():
    """Demonstrate cart with various product types."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Mixed Product Types")
    print("="*80)
    
    cart = ShoppingCart()
    
    # Add various products
    products = [
        Book("B001", "Clean Code", "Robert Martin", 464, 34.99, 0.7),
        Book("B002", "The Pragmatic Programmer", "Hunt & Thomas", 352, 39.99, 0.6),
        MusicAlbum("M001", "Pink Floyd", "The Dark Side of the Moon", 10, 14.99, 0.1),
        MusicAlbum("M002", "Miles Davis", "Kind of Blue", 5, 12.99, 0.1),
        SoftwareLicense("S001", "Microsoft Office 365", 99.99),
        SoftwareLicense("S002", "Adobe Creative Cloud", 54.99),
    ]
    
    for product in products:
        cart.add_product(product)
    
    print("\nFull Cart:")
    print(cart)
    
    # Breakdown by type
    physical_weight = sum(p.get_weight() for p in cart.get_items() 
                         if not isinstance(p, SoftwareLicense))
    digital_count = sum(1 for p in cart.get_items() 
                       if isinstance(p, SoftwareLicense))
    
    print(f"\n📊 Statistics:")
    print(f"   Physical items weight: {physical_weight:.2f}kg")
    print(f"   Digital items: {digital_count}")
    print(f"   Shipping required: {'Yes' if physical_weight > 0 else 'No'}")


def example_recommendation_system():
    """
    Demonstrate the product sequence analysis for recommendations.
    
    This is the OPTIONAL feature that analyzes which products are
    typically added together and in what order.
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Product Sequence Analysis (Recommendation System)")
    print("="*80)
    
    # Create products
    book_a = Book("B001", "Design Patterns", "GoF", 395, 44.99, 0.8)
    book_b = Book("B002", "Clean Code", "Robert Martin", 464, 34.99, 0.7)
    book_c = Book("B003", "Refactoring", "Martin Fowler", 448, 39.99, 0.75)
    album_d = MusicAlbum("M001", "The Beatles", "Abbey Road", 17, 15.99, 0.1)
    software_e = SoftwareLicense("S001", "IntelliJ IDEA", 149.99)
    
    # Simulate multiple shopping sessions
    # Cart 1: Customer interested in programming books
    cart1 = ShoppingCart()
    cart1.add_product(book_a)  # A added first
    cart1.add_product(book_b)  # B added after A
    cart1.add_product(software_e)  # E added after B
    
    # Cart 2: Similar pattern
    cart2 = ShoppingCart()
    cart2.add_product(book_a)  # A added first
    cart2.add_product(book_b)  # B added after A (pattern repeats!)
    cart2.add_product(book_c)  # C added after B
    
    # Cart 3: Different pattern
    cart3 = ShoppingCart()
    cart3.add_product(book_a)  # A added first
    cart3.add_product(album_d)  # D added after A
    cart3.add_product(book_b)  # B added after D
    
    # Cart 4: Another customer
    cart4 = ShoppingCart()
    cart4.add_product(book_c)  # C added first
    cart4.add_product(book_b)  # B added after C
    
    # Analyze the sequences
    carts = [cart1, cart2, cart3, cart4]
    stats = analyze_product_sequences(carts)
    
    # Create product name mapping for better readability
    product_names = {
        "B001": "Design Patterns",
        "B002": "Clean Code",
        "B003": "Refactoring",
        "M001": "Abbey Road Album",
        "S001": "IntelliJ IDEA"
    }
    
    # Print analysis
    print_sequence_analysis(stats, product_names)
    
    # Explain the results
    print("\n💡 How to use this data:")
    print("   - If customer adds 'Design Patterns', recommend 'Clean Code'")
    print("   - If customer adds 'Clean Code', they often added 'Design Patterns' first")
    print("   - Build 'Frequently Bought Together' features")
    print("   - Optimize product page suggestions")


def example_edge_cases():
    """Demonstrate error handling and edge cases."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Error Handling and Edge Cases")
    print("="*80)
    
    # Empty cart
    empty_cart = ShoppingCart()
    print(f"\n1. Empty cart:")
    print(f"   Is empty: {empty_cart.is_empty()}")
    print(f"   Total: €{empty_cart.get_total_price():.2f}")
    print(f"   Weight: {empty_cart.get_total_weight():.2f}kg")
    
    # Try to remove from empty cart
    result = empty_cart.remove_product("B001")
    print(f"   Remove from empty cart: {result}")
    
    # Invalid product values
    print(f"\n2. Input validation:")
    try:
        invalid_book = Book("B001", "Test", "Author", -100, 10.0, 0.5)
    except ValueError as e:
        print(f"   ✅ Caught error: {e}")
    
    try:
        negative_price = Book("B001", "Test", "Author", 100, -10.0, 0.5)
    except ValueError as e:
        print(f"   ✅ Caught error: {e}")
    
    try:
        negative_weight = MusicAlbum("M001", "Artist", "Album", 10, 15.0, -0.1)
    except ValueError as e:
        print(f"   ✅ Caught error: {e}")
    
    # Digital product weight
    print(f"\n3. Digital products:")
    software = SoftwareLicense("S001", "Software", 99.99)
    print(f"   Software weight: {software.get_weight()}kg (digital = no weight)")


def example_real_world_scenario():
    """Demonstrate a realistic e-commerce scenario."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Real-World E-Commerce Scenario")
    print("="*80)
    
    cart = ShoppingCart()
    
    print("\n📚 Customer browses programming section...")
    cart.add_product(Book("B001", "Clean Code", "Robert Martin", 464, 34.99, 0.7))
    cart.add_product(Book("B002", "Design Patterns", "GoF", 395, 44.99, 0.8))
    print(f"   Cart: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")
    
    print("\n🎵 Customer adds some music...")
    cart.add_product(MusicAlbum("M001", "Pink Floyd", "Dark Side", 10, 14.99, 0.1))
    print(f"   Cart: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")
    
    print("\n💻 Customer sees software recommendation...")
    cart.add_product(SoftwareLicense("S001", "IDE License", 149.99))
    print(f"   Cart: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")
    
    print("\n🤔 Customer changes mind about one book...")
    cart.remove_product("B002")
    print(f"   Cart: {cart.get_item_count()} items, €{cart.get_total_price():.2f}")
    
    print("\n📦 Checkout Summary:")
    print(f"   Items: {cart.get_item_count()}")
    print(f"   Subtotal: €{cart.get_total_price():.2f}")
    
    weight = cart.get_total_weight()
    shipping_cost = 5.00 if weight > 0 else 0.00
    print(f"   Shipping weight: {weight:.2f}kg")
    print(f"   Shipping cost: €{shipping_cost:.2f}")
    print(f"   Total: €{cart.get_total_price() + shipping_cost:.2f}")


def main():
    """Run all examples."""
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  SHOPPING CART SYSTEM - COMPREHENSIVE EXAMPLES".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    # Run all examples
    example_basic_usage()
    example_remove_products()
    example_mixed_products()
    example_recommendation_system()
    example_edge_cases()
    example_real_world_scenario()
    
    print("\n" + "="*80)
    print("✅ All examples completed successfully!")
    print("="*80)
    print("\nKey Features Demonstrated:")
    print("  ✓ Product creation (Books, Albums, Software)")
    print("  ✓ Shopping cart operations (add, remove, clear)")
    print("  ✓ Price and weight calculations")
    print("  ✓ Product sequence analysis for recommendations")
    print("  ✓ Error handling and validation")
    print("  ✓ Real-world e-commerce scenario")
    print("\n")


if __name__ == "__main__":
    main()
