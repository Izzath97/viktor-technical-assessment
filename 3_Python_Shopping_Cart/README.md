# Python Shopping Cart System

## Overview

This directory contains a complete object-oriented implementation of a shopping cart system for an online store. The system supports three types of products:

1. **Books** - Physical books with author, pages, and weight
2. **Music Albums (CDs)** - Physical music albums with artist, tracks, and weight
3. **Software Licenses** - Digital products with zero weight

## Features

### Core Functionality
- ✅ Create products of different types (Book, MusicAlbum, SoftwareLicense)
- ✅ Add products to shopping cart
- ✅ Remove products (single or all occurrences)
- ✅ Calculate total price of cart
- ✅ Calculate total weight of cart (excludes digital products)
- ✅ Track product addition sequence

### Advanced Features (Optional)
- ✅ **Product Sequence Analysis** - Analyze which products are typically added together and in what order
- ✅ **Recommendation System** - Identify patterns for "Frequently Bought Together" features
- ✅ **Extensible Design** - Easy to add new product types

## Files

- **`shopping_cart.py`** - Main implementation with all classes
- **`test_shopping_cart.py`** - Comprehensive unit tests
- **`examples.py`** - Usage examples and demonstrations
- **`README.md`** - This file

## Design Principles

### Object-Oriented Design
The system uses inheritance and polymorphism to create a flexible, extensible architecture:

```
Product (Abstract Base Class)
├── Book
├── MusicAlbum
└── SoftwareLicense
```

### Key Design Decisions

1. **Abstract Base Class (ABC)**: `Product` is an abstract class that defines the interface all products must implement
2. **Encapsulation**: Private attributes with property accessors
3. **Type Hints**: Full type annotations for clarity and IDE support
4. **Validation**: Input validation with meaningful error messages
5. **Immutability**: Product IDs and prices are read-only after creation
6. **Single Responsibility**: Each class has a clear, focused purpose

### Why This Design?

- **Extensibility**: Adding new product types requires minimal code changes
- **Maintainability**: Clear separation of concerns makes code easy to understand
- **Testability**: Each component can be tested independently
- **Reusability**: Components can be reused in different contexts
- **Type Safety**: Type hints catch errors early in development

## Usage

### Basic Usage

```python
from shopping_cart import Book, MusicAlbum, SoftwareLicense, ShoppingCart

# Create products
book = Book(
    product_id="B001",
    title="Clean Code",
    author="Robert C. Martin",
    num_pages=464,
    price=34.99,
    weight=0.7
)

album = MusicAlbum(
    product_id="M001",
    artist="The Beatles",
    title="Abbey Road",
    num_tracks=17,
    price=15.99,
    weight=0.1
)

software = SoftwareLicense(
    product_id="S001",
    software_name="PyCharm Professional",
    price=199.00
)

# Create shopping cart
cart = ShoppingCart()

# Add products
cart.add_product(book)
cart.add_product(album)
cart.add_product(software)

# Calculate totals
total_price = cart.get_total_price()  # 249.98
total_weight = cart.get_total_weight()  # 0.8 (software has 0 weight)

print(f"Total: €{total_price:.2f}")
print(f"Weight: {total_weight:.2f}kg")
```

### Product Sequence Analysis (Recommendation System)

```python
from shopping_cart import analyze_product_sequences, print_sequence_analysis

# Create multiple shopping carts (simulating customer behavior)
carts = []

# Customer 1
cart1 = ShoppingCart()
cart1.add_product(book_a)
cart1.add_product(book_b)
carts.append(cart1)

# Customer 2
cart2 = ShoppingCart()
cart2.add_product(book_a)
cart2.add_product(book_b)
carts.append(cart2)

# Customer 3
cart3 = ShoppingCart()
cart3.add_product(book_a)
cart3.add_product(album_c)
carts.append(cart3)

# Analyze sequences
stats = analyze_product_sequences(carts)

# Get insights
for product_id, stat in stats.items():
    print(f"{product_id} is most often added after {stat.most_common_predecessor}")
    print(f"  Occurrences: {stat.occurrences}")
```

## Running the Code

### Run Examples
```bash
python examples.py
```

This demonstrates:
- Basic cart operations
- Adding/removing products
- Mixed product types
- Product sequence analysis
- Error handling
- Real-world scenario

### Run Tests
```bash
# Using unittest
python test_shopping_cart.py

# Or using pytest (if installed)
pytest test_shopping_cart.py -v

# Or using Python's unittest module
python -m unittest test_shopping_cart.py -v
```

All tests include:
- Product creation and validation
- Shopping cart operations
- Price and weight calculations
- Product sequence analysis
- Edge cases and error handling

### Expected Test Output
```
test_add_duplicate_products ... ok
test_add_invalid_type ... ok
test_add_multiple_products ... ok
test_add_product ... ok
...

Ran 40 tests in 0.05s
OK
```

## Product Classes

### Book
```python
Book(
    product_id: str,    # Unique identifier
    title: str,         # Book title
    author: str,        # Author name
    num_pages: int,     # Number of pages (> 0)
    price: float,       # Price in euros (>= 0)
    weight: float       # Weight in kg (>= 0)
)
```

### MusicAlbum
```python
MusicAlbum(
    product_id: str,    # Unique identifier
    artist: str,        # Artist/band name
    title: str,         # Album title
    num_tracks: int,    # Number of tracks (> 0)
    price: float,       # Price in euros (>= 0)
    weight: float       # Weight in kg (>= 0)
)
```

### SoftwareLicense
```python
SoftwareLicense(
    product_id: str,    # Unique identifier
    software_name: str, # Software name
    price: float        # Price in euros (>= 0)
)
# Note: Digital products automatically have 0 weight
```

## ShoppingCart API

| Method | Description | Returns |
|--------|-------------|---------|
| `add_product(product)` | Add a product to cart | None |
| `remove_product(product_id)` | Remove first occurrence | bool (success) |
| `remove_all_products(product_id)` | Remove all occurrences | int (count removed) |
| `clear()` | Remove all items | None |
| `get_total_price()` | Calculate total price | float (euros) |
| `get_total_weight()` | Calculate total weight | float (kg) |
| `get_item_count()` | Count items in cart | int |
| `get_items()` | Get copy of all items | List[Product] |
| `is_empty()` | Check if cart is empty | bool |
| `get_product_sequence()` | Get product ID sequence | List[str] |

## Recommendation System

The `analyze_product_sequences()` function analyzes multiple shopping carts to identify patterns:

### How It Works
1. Tracks which products are added in sequence
2. For each product, counts how many times it follows other products
3. Identifies the most common predecessor for each product
4. Returns statistics for building recommendation features

### Use Cases
- **"Frequently Bought Together"** suggestions
- **"Customers who bought X also bought Y"** recommendations
- Product bundling strategies
- Inventory planning
- Marketing insights

### Example Output
```
Product B is most often added AFTER: Product A
  Occurrences: 5 times

Product C is most often added AFTER: Product A
  Occurrences: 3 times
```

## Testing Strategy

The test suite covers:

1. **Unit Tests** - Each class tested independently
2. **Integration Tests** - Components working together
3. **Edge Cases** - Empty carts, invalid inputs, boundary conditions
4. **Error Handling** - Proper exception raising and handling
5. **Recommendation System** - Sequence analysis with various patterns

### Test Coverage
- ✅ Product creation and validation
- ✅ Price and weight calculations
- ✅ Adding/removing products
- ✅ Cart operations (clear, empty checks)
- ✅ Product sequences
- ✅ Recommendation analysis
- ✅ Error conditions
- ✅ String representations

## Extensibility

### Adding a New Product Type

To add a new product type (e.g., `DigitalBook`):

```python
class DigitalBook(Product):
    """Represents a digital/eBook."""
    
    def __init__(self, product_id: str, title: str, 
                 author: str, price: float, file_format: str):
        super().__init__(product_id, price)
        self.title = title
        self.author = author
        self.file_format = file_format
    
    def get_weight(self) -> float:
        """Digital products have no weight."""
        return 0.0
    
    def get_description(self) -> str:
        return f"eBook: '{self.title}' by {self.author} ({self.file_format})"
```

**No changes needed to `ShoppingCart` or other classes!** This is the power of polymorphism.

## Performance Considerations

- **O(1)** - Adding products
- **O(n)** - Removing products (linear search)
- **O(n)** - Calculating totals
- **O(n*m)** - Sequence analysis (n = carts, m = avg items per cart)

For production use with large datasets, consider:
- Using a dictionary for O(1) product lookup by ID
- Caching total calculations
- Batch operations for bulk updates

## Requirements

- **Python 3.7+** (for type hints and dataclasses)
- No external dependencies for core functionality
- Optional: `pytest` for running tests (though `unittest` works too)

## Code Quality

This code follows:
- ✅ **PEP 8** - Python style guide
- ✅ **Type hints** - Full type annotations
- ✅ **Docstrings** - Comprehensive documentation
- ✅ **SOLID principles** - Clean architecture
- ✅ **DRY** - Don't Repeat Yourself
- ✅ **KISS** - Keep It Simple, Stupid
- ✅ **Comments** - Explaining why, not what

## Future Enhancements

Possible extensions (not implemented to keep scope manageable):
- Product quantities (instead of duplicate instances)
- Discount codes and promotions
- Tax calculations
- Shipping cost estimation
- Persistent storage (database/file)
- User authentication and order history
- Product reviews and ratings

---

**Author:** Mohamed Izzath  
**Date:** November 2, 2025  
**Python Version:** 3.7+
