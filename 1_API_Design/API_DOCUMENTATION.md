# RESTful API Documentation
## Book Analysis Application

**Version:** 1.0  
**Base URL:** `https://api.bookanalysis.com/v1`  
**Date:** November 2, 2025

---

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Common Response Codes](#common-response-codes)
4. [Endpoints](#endpoints)
   - [Books Management](#books-management)
   - [Book Contents](#book-contents)
   - [Book Processing](#book-processing)

---

## Overview

This API provides functionality for managing a digital library and performing natural language processing analysis on books. The API follows RESTful principles and uses JSON for request and response bodies.

### Key Features
- Full CRUD operations for books
- Advanced filtering, sorting, and pagination
- File upload for book contents
- Asynchronous processing for linguistic analysis

---

## Authentication

All API requests require authentication using Bearer tokens:

```
Authorization: Bearer <your_access_token>
```

*(Note: Authentication implementation details would be specified in production)*

---

## Common Response Codes

| Status Code | Description |
|------------|-------------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource successfully created |
| 202 | Accepted - Request accepted for processing |
| 204 | No Content - Request succeeded, no content to return |
| 400 | Bad Request - Invalid request parameters |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource does not exist |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server error |

---

## Endpoints

### Books Management

#### 1. Create a Book

**Endpoint:** `POST /books/`

**Description:** Creates a new book in the library.

**Request Body:**
```json
{
  "name": "The Lord of the Rings",
  "author": "J.R.R. Tolkien",
  "publisher": "Allen & Unwin",
  "publicationDate": "1954-07-29",
  "isbn": "978-0-618-00222-1",
  "coverPhoto": "https://example.com/cover.jpg"
}
```

**Request Body Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Title of the book (max 255 chars) |
| author | string | Yes | Author name (max 255 chars) |
| publisher | string | Yes | Publisher name (max 255 chars) |
| publicationDate | string | Yes | Publication date (ISO 8601: YYYY-MM-DD) |
| isbn | string | Yes | ISBN number (10 or 13 digits) |
| coverPhoto | string | No | URL to cover photo (max 2048 chars) |

**Responses:**

**201 Created** - Book successfully created
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "The Lord of the Rings",
  "author": "J.R.R. Tolkien",
  "publisher": "Allen & Unwin",
  "publicationDate": "1954-07-29",
  "isbn": "978-0-618-00222-1",
  "coverPhoto": "https://example.com/cover.jpg",
  "createdAt": "2025-11-02T10:30:00Z",
  "updatedAt": "2025-11-02T10:30:00Z",
  "hasContent": false,
  "processingStatus": null
}
```

**400 Bad Request** - Invalid input data
```json
{
  "error": "Validation Error",
  "details": {
    "isbn": ["Invalid ISBN format"],
    "publicationDate": ["Date cannot be in the future"]
  }
}
```

**409 Conflict** - Book with same ISBN already exists
```json
{
  "error": "Conflict",
  "message": "A book with ISBN '978-0-618-00222-1' already exists"
}
```

---

#### 2. Update Book Cover Photo

**Endpoint:** `PATCH /books/{bookId}/cover-photo/`

**Description:** Updates only the cover photo of an existing book.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Request Body:**
```json
{
  "coverPhoto": "https://example.com/new-cover.jpg"
}
```

**Request Body Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| coverPhoto | string | Yes | URL to new cover photo (max 2048 chars) |

**Responses:**

**200 OK** - Cover photo successfully updated
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "The Lord of the Rings",
  "author": "J.R.R. Tolkien",
  "publisher": "Allen & Unwin",
  "publicationDate": "1954-07-29",
  "isbn": "978-0-618-00222-1",
  "coverPhoto": "https://example.com/new-cover.jpg",
  "createdAt": "2025-11-02T10:30:00Z",
  "updatedAt": "2025-11-02T11:15:00Z",
  "hasContent": false,
  "processingStatus": null
}
```

**404 Not Found** - Book does not exist
```json
{
  "error": "Not Found",
  "message": "No book found with ID '550e8400-e29b-41d4-a716-446655440000'"
}
```

**400 Bad Request** - Invalid URL format
```json
{
  "error": "Validation Error",
  "details": {
    "coverPhoto": ["Invalid URL format"]
  }
}
```

---

#### 3. List Books

**Endpoint:** `GET /books/`

**Description:** Retrieves a paginated list of books with optional filtering and sorting.

**Query Parameters:**

**Pagination:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number (minimum: 1) |
| pageSize | integer | 20 | Number of items per page (1-100) |

**Filtering:**
All book fields can be filtered using the following operators:
| Parameter Format | Description | Example |
|-----------------|-------------|---------|
| {field} | Exact match | `?author=J.R.R. Tolkien` |
| {field}__contains | Contains substring (case-insensitive) | `?name__contains=lord` |
| {field}__in | Match any value in comma-separated list | `?author__in=Tolkien,Rowling` |
| {field}__gte | Greater than or equal | `?publicationDate__gte=2000-01-01` |
| {field}__lte | Less than or equal | `?publicationDate__lte=2020-12-31` |

**Sorting:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| sort | Sort by field(s), comma-separated | `?sort=name,-publicationDate` |
| | Prefix with `-` for descending order | (sorts by name ASC, then date DESC) |

**Example Request:**
```
GET /books/?page=1&pageSize=10&author__contains=tolkien&publicationDate__gte=1950-01-01&sort=-publicationDate,name
```

**Responses:**

**200 OK** - Books successfully retrieved
```json
{
  "count": 150,
  "page": 1,
  "pageSize": 10,
  "totalPages": 15,
  "next": "https://api.bookanalysis.com/v1/books/?page=2&pageSize=10",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "The Lord of the Rings",
      "author": "J.R.R. Tolkien",
      "publisher": "Allen & Unwin",
      "publicationDate": "1954-07-29",
      "isbn": "978-0-618-00222-1",
      "coverPhoto": "https://example.com/cover.jpg",
      "createdAt": "2025-11-02T10:30:00Z",
      "updatedAt": "2025-11-02T10:30:00Z",
      "hasContent": true,
      "processingStatus": "completed"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "name": "The Hobbit",
      "author": "J.R.R. Tolkien",
      "publisher": "George Allen & Unwin",
      "publicationDate": "1937-09-21",
      "isbn": "978-0-547-92822-7",
      "coverPhoto": "https://example.com/hobbit-cover.jpg",
      "createdAt": "2025-11-02T09:15:00Z",
      "updatedAt": "2025-11-02T09:15:00Z",
      "hasContent": true,
      "processingStatus": "processing"
    }
  ]
}
```

**400 Bad Request** - Invalid query parameters
```json
{
  "error": "Bad Request",
  "details": {
    "pageSize": ["Must be between 1 and 100"],
    "sort": ["Invalid field: 'invalidField'"]
  }
}
```

---

#### 4. Get Single Book

**Endpoint:** `GET /books/{bookId}/`

**Description:** Retrieves a single book by its unique identifier.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Responses:**

**200 OK** - Book successfully retrieved
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "The Lord of the Rings",
  "author": "J.R.R. Tolkien",
  "publisher": "Allen & Unwin",
  "publicationDate": "1954-07-29",
  "isbn": "978-0-618-00222-1",
  "coverPhoto": "https://example.com/cover.jpg",
  "createdAt": "2025-11-02T10:30:00Z",
  "updatedAt": "2025-11-02T10:30:00Z",
  "hasContent": true,
  "processingStatus": "completed",
  "contentMetadata": {
    "fileName": "lotr_complete.pdf",
    "fileSize": 2457600,
    "uploadedAt": "2025-11-02T11:00:00Z"
  }
}
```

**404 Not Found** - Book does not exist
```json
{
  "error": "Not Found",
  "message": "No book found with ID '550e8400-e29b-41d4-a716-446655440000'"
}
```

---

#### 5. Update Book

**Endpoint:** `PUT /books/{bookId}/`

**Description:** Updates all fields of an existing book (full update).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Request Body:**
```json
{
  "name": "The Lord of the Rings: The Fellowship of the Ring",
  "author": "J.R.R. Tolkien",
  "publisher": "Allen & Unwin",
  "publicationDate": "1954-07-29",
  "isbn": "978-0-618-00222-1",
  "coverPhoto": "https://example.com/updated-cover.jpg"
}
```

**Responses:**

**200 OK** - Book successfully updated
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "The Lord of the Rings: The Fellowship of the Ring",
  "author": "J.R.R. Tolkien",
  "publisher": "Allen & Unwin",
  "publicationDate": "1954-07-29",
  "isbn": "978-0-618-00222-1",
  "coverPhoto": "https://example.com/updated-cover.jpg",
  "createdAt": "2025-11-02T10:30:00Z",
  "updatedAt": "2025-11-02T12:00:00Z",
  "hasContent": true,
  "processingStatus": "completed"
}
```

**404 Not Found** - Book does not exist

**400 Bad Request** - Invalid input data

---

#### 6. Partially Update Book

**Endpoint:** `PATCH /books/{bookId}/`

**Description:** Updates specific fields of an existing book (partial update).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Request Body (any combination of fields):**
```json
{
  "name": "The Lord of the Rings: Updated Edition",
  "publisher": "HarperCollins"
}
```

**Responses:**

**200 OK** - Book successfully updated

**404 Not Found** - Book does not exist

**400 Bad Request** - Invalid input data

---

#### 7. Delete Book

**Endpoint:** `DELETE /books/{bookId}/`

**Description:** Permanently deletes a book and all associated data (content, processing results).

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Responses:**

**204 No Content** - Book successfully deleted (no response body)

**404 Not Found** - Book does not exist
```json
{
  "error": "Not Found",
  "message": "No book found with ID '550e8400-e29b-41d4-a716-446655440000'"
}
```

---

### Book Contents

#### 8. Upload Book Content

**Endpoint:** `POST /books/{bookId}/content/`

**Description:** Uploads the full text content of a book as a file. Supported formats: PDF, EPUB, TXT, DOCX.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Request:**
- **Content-Type:** `multipart/form-data`
- **Max File Size:** 50 MB

**Form Data:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | The book content file |

**Example Request:**
```bash
curl -X POST \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/book.pdf" \
  https://api.bookanalysis.com/v1/books/550e8400-e29b-41d4-a716-446655440000/content/
```

**Responses:**

**201 Created** - Content successfully uploaded
```json
{
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "contentId": "770e8400-e29b-41d4-a716-446655440002",
  "fileName": "lotr_complete.pdf",
  "fileSize": 2457600,
  "contentType": "application/pdf",
  "uploadedAt": "2025-11-02T11:00:00Z",
  "status": "uploaded",
  "message": "Content uploaded successfully. You can now process this book."
}
```

**404 Not Found** - Book does not exist

**400 Bad Request** - Invalid file format or size
```json
{
  "error": "Bad Request",
  "message": "Unsupported file format. Supported formats: PDF, EPUB, TXT, DOCX"
}
```

**413 Payload Too Large** - File exceeds size limit
```json
{
  "error": "Payload Too Large",
  "message": "File size exceeds maximum limit of 50 MB"
}
```

---

#### 9. Download Book Content

**Endpoint:** `GET /books/{bookId}/content/`

**Description:** Downloads the original uploaded content file.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Responses:**

**200 OK** - File successfully retrieved
- **Content-Type:** Original file MIME type
- **Content-Disposition:** `attachment; filename="book_content.pdf"`
- **Body:** Binary file data

**404 Not Found** - Book or content does not exist
```json
{
  "error": "Not Found",
  "message": "No content found for book with ID '550e8400-e29b-41d4-a716-446655440000'"
}
```

---

#### 10. Delete Book Content

**Endpoint:** `DELETE /books/{bookId}/content/`

**Description:** Deletes the uploaded content and all associated processing results.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Responses:**

**204 No Content** - Content successfully deleted

**404 Not Found** - Book or content does not exist

---

### Book Processing

#### 11. Start Book Processing

**Endpoint:** `POST /books/{bookId}/process/`

**Description:** Initiates asynchronous linguistic analysis of a book's content. Returns immediately with a job ID for tracking progress.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Request Body (optional):**
```json
{
  "analysisTypes": ["sentiment", "topics", "entities", "keywords", "summary"],
  "language": "en",
  "priority": "normal"
}
```

**Request Body Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| analysisTypes | array | No | all types | Types of analysis to perform |
| language | string | No | auto-detect | ISO 639-1 language code |
| priority | string | No | normal | Processing priority: low, normal, high |

**Responses:**

**202 Accepted** - Processing job created and queued
```json
{
  "jobId": "880e8400-e29b-41d4-a716-446655440003",
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "createdAt": "2025-11-02T12:00:00Z",
  "estimatedCompletionTime": "2025-11-02T12:15:00Z",
  "statusUrl": "/books/550e8400-e29b-41d4-a716-446655440000/process/880e8400-e29b-41d4-a716-446655440003/",
  "message": "Processing job created successfully. Use the statusUrl to track progress."
}
```

**404 Not Found** - Book does not exist

**400 Bad Request** - Book has no content or invalid parameters
```json
{
  "error": "Bad Request",
  "message": "Cannot process book: No content has been uploaded"
}
```

**409 Conflict** - Book is already being processed
```json
{
  "error": "Conflict",
  "message": "This book is already being processed. Job ID: 880e8400-e29b-41d4-a716-446655440003"
}
```

---

#### 12. Get Processing Status

**Endpoint:** `GET /books/{bookId}/process/{jobId}/`

**Description:** Retrieves the current status and progress of a processing job.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |
| jobId | UUID | Unique identifier of the processing job |

**Responses:**

**200 OK** - Status successfully retrieved

**Processing (in progress):**
```json
{
  "jobId": "880e8400-e29b-41d4-a716-446655440003",
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "currentStep": "Extracting entities",
  "createdAt": "2025-11-02T12:00:00Z",
  "startedAt": "2025-11-02T12:01:00Z",
  "estimatedCompletionTime": "2025-11-02T12:15:00Z"
}
```

**Completed:**
```json
{
  "jobId": "880e8400-e29b-41d4-a716-446655440003",
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "createdAt": "2025-11-02T12:00:00Z",
  "startedAt": "2025-11-02T12:01:00Z",
  "completedAt": "2025-11-02T12:14:30Z",
  "resultsUrl": "/books/550e8400-e29b-41d4-a716-446655440000/insights/"
}
```

**Failed:**
```json
{
  "jobId": "880e8400-e29b-41d4-a716-446655440003",
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "progress": 30,
  "error": "Language detection failed",
  "createdAt": "2025-11-02T12:00:00Z",
  "startedAt": "2025-11-02T12:01:00Z",
  "failedAt": "2025-11-02T12:05:00Z"
}
```

**404 Not Found** - Book or job does not exist

---

#### 13. Cancel Processing Job

**Endpoint:** `DELETE /books/{bookId}/process/{jobId}/`

**Description:** Cancels an ongoing processing job.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |
| jobId | UUID | Unique identifier of the processing job |

**Responses:**

**200 OK** - Job successfully cancelled
```json
{
  "jobId": "880e8400-e29b-41d4-a716-446655440003",
  "status": "cancelled",
  "message": "Processing job cancelled successfully"
}
```

**404 Not Found** - Book or job does not exist

**409 Conflict** - Job already completed or failed
```json
{
  "error": "Conflict",
  "message": "Cannot cancel job: Job has already completed"
}
```

---

#### 14. Get Processing Results (Insights)

**Endpoint:** `GET /books/{bookId}/insights/`

**Description:** Retrieves the linguistic analysis results for a processed book.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| include | string | Comma-separated list of insight types to include |

**Responses:**

**200 OK** - Insights successfully retrieved
```json
{
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "bookName": "The Lord of the Rings",
  "processedAt": "2025-11-02T12:14:30Z",
  "language": "en",
  "insights": {
    "sentiment": {
      "overall": "positive",
      "score": 0.72,
      "distribution": {
        "positive": 65,
        "neutral": 25,
        "negative": 10
      }
    },
    "keywords": [
      {"keyword": "ring", "frequency": 156, "relevance": 0.95},
      {"keyword": "quest", "frequency": 89, "relevance": 0.87},
      {"keyword": "friendship", "frequency": 67, "relevance": 0.81}
    ],
    "topics": [
      {"topic": "Adventure", "confidence": 0.92},
      {"topic": "Fantasy", "confidence": 0.89},
      {"topic": "Heroism", "confidence": 0.85}
    ],
    "entities": {
      "persons": ["Frodo", "Gandalf", "Aragorn"],
      "locations": ["Shire", "Mordor", "Gondor"],
      "organizations": ["Fellowship"]
    },
    "summary": "An epic tale of adventure and friendship...",
    "statistics": {
      "wordCount": 481043,
      "sentenceCount": 28560,
      "averageWordsPerSentence": 16.8,
      "readingLevel": "Advanced"
    }
  }
}
```

**404 Not Found** - Book does not exist or has not been processed
```json
{
  "error": "Not Found",
  "message": "No processing results found for this book"
}
```

---

#### 15. List All Processing Jobs

**Endpoint:** `GET /books/{bookId}/process/`

**Description:** Retrieves all processing jobs for a specific book.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bookId | UUID | Unique identifier of the book |

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| status | string | Filter by status: queued, processing, completed, failed, cancelled |

**Responses:**

**200 OK** - Jobs successfully retrieved
```json
{
  "bookId": "550e8400-e29b-41d4-a716-446655440000",
  "count": 3,
  "jobs": [
    {
      "jobId": "880e8400-e29b-41d4-a716-446655440003",
      "status": "completed",
      "createdAt": "2025-11-02T12:00:00Z",
      "completedAt": "2025-11-02T12:14:30Z"
    },
    {
      "jobId": "880e8400-e29b-41d4-a716-446655440004",
      "status": "failed",
      "createdAt": "2025-11-01T15:30:00Z",
      "failedAt": "2025-11-01T15:35:00Z"
    }
  ]
}
```

**404 Not Found** - Book does not exist

---

## Design Decisions & Rationale

### 1. RESTful Principles
- **Resource-based URLs:** `/books/`, `/books/{id}/content/`, `/books/{id}/process/`
- **HTTP verbs:** Proper use of GET, POST, PUT, PATCH, DELETE
- **Stateless:** Each request contains all necessary information
- **Hypermedia:** Links to related resources (next/previous, statusUrl, resultsUrl)

### 2. Asynchronous Processing
- **Non-blocking design:** Processing returns 202 Accepted immediately with job ID
- **Status tracking:** Dedicated endpoint for polling job status
- **Cancellation support:** Allows users to cancel long-running jobs
- **Separation of concerns:** Processing jobs are independent resources

### 3. Pagination & Filtering
- **Cursor-based pagination:** Efficient for large datasets
- **Flexible filtering:** Multiple operators for different query types
- **Multi-field sorting:** Supports complex sorting requirements
- **Performance:** Query parameters allow efficient database queries

### 4. Error Handling
- **Consistent structure:** All errors follow the same format
- **Descriptive messages:** Clear explanations for failures
- **Validation details:** Field-level error information
- **Appropriate status codes:** Semantic HTTP status codes

### 5. Versioning
- **URL versioning:** `/v1/` prefix allows backward compatibility
- **Future-proof:** Easy to introduce breaking changes in v2

### 6. File Upload
- **Multipart form data:** Standard for file uploads
- **Size limits:** Prevents abuse and ensures system stability
- **Format validation:** Ensures processable content
- **Separate endpoint:** Clear separation of concerns

---

## Future Enhancements

1. **Webhook notifications:** Notify clients when processing completes
2. **Batch operations:** Process multiple books simultaneously
3. **Rate limiting:** Prevent abuse with request throttling
4. **GraphQL endpoint:** Alternative query interface for complex queries
5. **Real-time updates:** WebSocket support for live processing status
6. **Advanced search:** Full-text search across book content
7. **Comparison API:** Compare linguistic insights between books

---

**Documentation Version:** 1.0  
**Last Updated:** November 2, 2025
