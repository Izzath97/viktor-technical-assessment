# Viktor Technical Assessment

**Candidate:** Mohamed Izzath  
**Date:** November 2, 2025  
**Time Limit:** 3 Hours

## Overview

This submission contains solutions to a three-part technical assessment covering:
1. RESTful API Design
2. SQL Database Queries
3. Python Object-Oriented Programming

## Project Structure

```
viktor_assessment/
├── README.md                          # This file
├── 1_API_Design/
│   ├── API_DOCUMENTATION.md          # Complete RESTful API specification
│   └── README.md                      # API design notes and rationale
├── 2_SQL_Queries/
│   ├── queries.sql                    # SQL queries with explanations
│   ├── schema.sql                     # Database schema for reference
│   └── README.md                      # SQL solutions overview
└── 3_Python_Shopping_Cart/
    ├── shopping_cart.py               # Main implementation
    ├── test_shopping_cart.py          # Unit tests
    ├── examples.py                    # Usage examples
    └── README.md                      # Implementation guide
```

## Deliverables

### Part 1: RESTful API Design
- **Location:** `1_API_Design/API_DOCUMENTATION.md`
- **Description:** Complete API specification for a book analysis application including:
  - CRUD operations for books
  - File upload for book contents
  - Non-blocking processing endpoints
  - Pagination, filtering, and sorting

### Part 2: SQL Queries
- **Location:** `2_SQL_Queries/queries.sql`
- **Description:** Three SQL queries for company/project/employee database:
  1. Get names of running projects
  2. Count finished projects per company
  3. Find companies with 2+ projects having the same name

### Part 3: Python Shopping Cart
- **Location:** `3_Python_Shopping_Cart/shopping_cart.py`
- **Description:** Object-oriented shopping cart system with:
  - Product classes (Book, MusicAlbum, SoftwareLicense)
  - Shopping cart with add/remove/calculate operations
  - Product recommendation system (optional feature)

## Key Features

- **Clean, Production-Ready Code:** Well-structured, documented, and following Python best practices
- **Comprehensive Documentation:** Each section includes detailed explanations and rationale
- **Extensive Testing:** Unit tests and examples demonstrate functionality
- **Extensible Design:** Architecture allows for easy future enhancements
- **Professional Standards:** Follows industry best practices and design patterns

## Running the Python Code

```bash
# Navigate to the Python directory
cd 3_Python_Shopping_Cart

# Run the examples
python examples.py

# Run the unit tests
python -m pytest test_shopping_cart.py -v
```

## Technologies Used

- **Python 3.x** - Core programming language
- **REST API Design Principles** - Industry-standard API architecture
- **SQL (PostgreSQL/MySQL compatible)** - Database query language
- **Object-Oriented Design** - Clean architecture patterns

## Notes

All solutions are designed with:
- **Scalability** in mind
- **Maintainability** as a priority
- **Best practices** implementation
- **Clear documentation** for easy understanding
- **Real-world applicability** for production environments

## Contact

For any questions or clarifications about this submission, please contact:
- **Email:** [Your email]
- **GitHub:** [Your GitHub profile]

---

**Submission Date:** November 2, 2025
