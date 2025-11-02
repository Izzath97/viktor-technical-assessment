# Shopping Cart API

A professional RESTful API for managing a store that sells books, music albums (CDs), and software licenses, with integrated shopping cart functionality and product recommendation system.

## 🎯 Features

### Core Functionality
- **Product Management**: Create, read, update, and delete books, music albums, and software licenses
- **Shopping Cart**: Add/remove/update items, calculate total price and weight
- **Clean Architecture**: Abstract base class for products with proper inheritance
- **Type Safety**: UUID primary keys and proper validation

### Advanced Features
- **Recommendation System**: Analyzes product addition patterns
- **Sequence Analysis**: Finds most common products added after each product
- **Frequently Bought Together**: Discovers product combinations
- **Extensible Design**: Easy to add new product types

## 🚀 Quick Start with Docker

### Prerequisites
- Docker Desktop installed and running
- Docker Compose V2+

### 1. Start the Application

```bash
cd shopping_cart
docker compose up --build
```

The API will be available at http://localhost:8000/api/

### 2. Create Sample Data (Optional)

```bash
# Access the running container
docker compose exec web python manage.py shell

# Create sample products
from shop.models import Book, MusicAlbum, SoftwareLicense
from decimal import Decimal

book = Book.objects.create(
    title="Clean Code",
    author="Robert C. Martin",
    number_of_pages=464,
    price=Decimal('42.50'),
    weight=Decimal('0.8')
)

album = MusicAlbum.objects.create(
    artist="The Beatles",
    title="Abbey Road",
    number_of_tracks=17,
    price=Decimal('15.99'),
    weight=Decimal('0.1')
)

software = SoftwareLicense.objects.create(
    name="IntelliJ IDEA Professional",
    price=Decimal('199.00')
)
```

## 📋 API Endpoints

### Products

#### Books
- `GET /api/books/` - List all books
- `POST /api/books/` - Create a new book
- `GET /api/books/{id}/` - Get book details
- `PUT /api/books/{id}/` - Update book
- `PATCH /api/books/{id}/` - Partial update
- `DELETE /api/books/{id}/` - Delete book

#### Music Albums
- `GET /api/music-albums/` - List all music albums
- `POST /api/music-albums/` - Create a new music album
- `GET /api/music-albums/{id}/` - Get album details
- `PUT /api/music-albums/{id}/` - Update album
- `DELETE /api/music-albums/{id}/` - Delete album

#### Software Licenses
- `GET /api/software-licenses/` - List all licenses
- `POST /api/software-licenses/` - Create a new license
- `GET /api/software-licenses/{id}/` - Get license details
- `PUT /api/software-licenses/{id}/` - Update license
- `DELETE /api/software-licenses/{id}/` - Delete license

### Shopping Cart

#### Cart Management
- `GET /api/carts/` - List all carts
- `POST /api/carts/` - Create a new cart
- `GET /api/carts/{id}/` - Get cart details (includes total_price and total_weight)
- `DELETE /api/carts/{id}/` - Delete cart

#### Cart Operations
- `POST /api/carts/{id}/add_item/` - Add product to cart
- `POST /api/carts/{id}/remove_item/` - Remove product from cart
- `POST /api/carts/{id}/update_item/` - Update item quantity
- `POST /api/carts/{id}/clear/` - Clear all items from cart

### Recommendation System
- `GET /api/carts/analyze_sequences/` - Analyze product addition sequences
- `GET /api/carts/recommendations/?product_id={uuid}` - Get recommendations for a product
- `GET /api/carts/frequently_bought_together/?min_frequency=2` - Get product pairs

## 🔧 API Usage Examples

### Create a Book

```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Design Patterns",
    "author": "Gang of Four",
    "number_of_pages": 395,
    "price": "54.99",
    "weight": "1.2"
  }'
```

### Create a Cart

```bash
curl -X POST http://localhost:8000/api/carts/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Add Item to Cart

```bash
curl -X POST http://localhost:8000/api/carts/{cart_id}/add_item/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_type": "book",
    "product_id": "{book_uuid}",
    "quantity": 2
  }'
```

### Get Cart Details (with totals)

```bash
curl http://localhost:8000/api/carts/{cart_id}/
```

Response includes:
```json
{
  "id": "...",
  "is_active": true,
  "items": [...],
  "total_price": "109.98",
  "total_weight": "2.400",
  "items_count": 2,
  "created_at": "...",
  "updated_at": "..."
}
```

### Get Product Recommendations

```bash
curl "http://localhost:8000/api/carts/recommendations/?product_id={product_uuid}&limit=5"
```

### Analyze Product Sequences

```bash
curl http://localhost:8000/api/carts/analyze_sequences/
```

Response shows which products are most commonly added after each product:
```json
[
  {
    "product_id": "...",
    "most_common_next_product": "...",
    "occurrence_count": 5
  }
]
```

## 🧪 Testing

### Run All Tests

```bash
docker compose exec web pytest
```

### Run Specific Test Class

```bash
docker compose exec web pytest shop/tests.py::CartModelTests
```

### Run with Coverage

```bash
docker compose exec web pytest --cov=shop
```

### Code Quality Check

```bash
docker compose exec web flake8
```

## 📁 Project Structure

```
shopping_cart/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings (Docker-aware)
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── shop/                   # Main application
│   ├── models.py          # Product and Cart models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API viewsets
│   ├── urls.py            # API routing
│   ├── admin.py           # Django admin configuration
│   ├── recommendations.py # Recommendation algorithms
│   └── tests.py           # Comprehensive test suite
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container setup
├── requirements.txt       # Python dependencies
├── pytest.ini             # Test configuration
├── .flake8                # Code quality rules
└── README.md              # This file
```

## 🏗️ Architecture & Design

### Design Patterns Used

1. **Abstract Factory Pattern**: `Product` abstract base class
2. **Repository Pattern**: Django ORM provides data access layer
3. **Strategy Pattern**: Different product types with polymorphic behavior
4. **Generic Relations**: ContentType framework for flexible cart items

### SOLID Principles

- **Single Responsibility**: Each model has one clear purpose
- **Open/Closed**: Easy to extend with new product types
- **Liskov Substitution**: All products are substitutable
- **Interface Segregation**: Clean, focused interfaces
- **Dependency Inversion**: Depends on abstractions (Product base class)

### Key Features

- **UUID Primary Keys**: Better for distributed systems and security
- **Decimal for Money**: Precise financial calculations
- **Database Indexes**: Optimized queries on frequently searched fields
- **Generic Foreign Keys**: Support any product type in cart
- **Proper Validation**: Django validators for data integrity

## 🔍 Recommendation System

The recommendation system analyzes cart data to provide insights:

### 1. Product Sequence Analysis

Tracks the order in which products are added to carts:

```python
# Example: If carts show
# Cart 1: [A, B, C]
# Cart 2: [A, B, D]
# Cart 3: [A, C, B]

# Result: B is most commonly added after A (2 times)
```

### 2. Product Recommendations

Given a product, suggests what customers typically add next:

```python
get_product_recommendations(product_id, carts, limit=5)
# Returns top 5 products frequently added after this one
```

### 3. Frequently Bought Together

Discovers product pairs that appear together in carts:

```python
find_frequently_bought_together(carts, min_frequency=2)
# Returns product combinations appearing 2+ times
```

## 🐳 Docker Commands

### Start services

```bash
docker compose up -d
```

### Stop services

```bash
docker compose down
```

### View logs

```bash
docker compose logs -f web
```

### Rebuild after changes

```bash
docker compose up --build
```

### Run Django commands

```bash
# Create superuser
docker compose exec web python manage.py createsuperuser

# Run migrations
docker compose exec web python manage.py migrate

# Django shell
docker compose exec web python manage.py shell
```

### Access database

```bash
docker compose exec db psql -U postgres -d shopping_cart
```

### Clean up

```bash
docker compose down -v  # Remove volumes too
```

## 📊 Models Overview

### Product (Abstract Base)
- `id` (UUID)
- `price` (Decimal)
- `created_at`, `updated_at`
- `get_weight()` method

### Book
- All Product fields
- `title`, `author`
- `number_of_pages`
- `weight`

### MusicAlbum
- All Product fields
- `artist`, `title`
- `number_of_tracks`
- `weight`

### SoftwareLicense
- All Product fields
- `name`
- `license_key`
- `valid_until`
- No weight (digital product)

### Cart
- `id` (UUID)
- `is_active`
- `created_at`, `updated_at`
- Methods: `add_item()`, `remove_item()`, `clear()`
- Calculations: `get_total_price()`, `get_total_weight()`

### CartItem
- Links any product to a cart
- `quantity`
- `added_at` timestamp
- Uses Generic Foreign Key for flexibility

## 💡 Usage Tips

### Adding New Product Types

1. Create a new model inheriting from `Product`
2. Implement `get_weight()` method
3. Create serializer
4. Add viewset
5. Register in admin
6. That's it! Cart automatically supports it

### Performance Optimization

- Database indexes on frequently queried fields
- Pagination enabled (20 items per page)
- Use `select_related()` and `prefetch_related()` for complex queries

### Production Considerations

1. Change `SECRET_KEY` in environment
2. Set `DEBUG=False`
3. Configure `ALLOWED_HOSTS`
4. Use proper database credentials
5. Set up SSL/TLS
6. Configure backup strategy
7. Scale with multiple workers

## 🧩 Extension Ideas

- Add user authentication
- Implement order history
- Add discount/coupon system
- Integrate payment gateway
- Add product categories
- Implement inventory management
- Add product reviews and ratings
- Real-time cart synchronization

## 📝 Development

### Local Development (without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Running Tests Locally

```bash
pytest
pytest --cov=shop  # With coverage
flake8  # Code quality
```

## 📄 License

This project is created as part of the Viktor Technical Assessment.

## 👨‍💻 Code Quality

- **Type Hints**: Used throughout for better IDE support
- **Docstrings**: Comprehensive documentation
- **Clean Code**: Follows PEP 8 and Django best practices
- **Test Coverage**: Comprehensive test suite
- **SOLID Principles**: Applied consistently
- **DRY**: No code duplication
- **Professional Structure**: Production-ready organization
