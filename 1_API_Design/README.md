# API Design - Overview

## Design Philosophy

This RESTful API design follows industry best practices and modern API design principles to create a scalable, maintainable, and user-friendly interface for the book analysis application.

## Key Design Principles Applied

### 1. Resource-Oriented Architecture
- Books are treated as primary resources
- Sub-resources (content, processing jobs, insights) are logically nested
- Clear hierarchy: `/books/{id}/content/`, `/books/{id}/process/{jobId}/`

### 2. HTTP Semantics
- **GET**: Retrieve resources (idempotent, cacheable)
- **POST**: Create new resources or initiate actions
- **PUT**: Complete replacement of resources
- **PATCH**: Partial updates (e.g., cover photo only)
- **DELETE**: Remove resources

### 3. Asynchronous Processing Pattern
The processing endpoints implement a standard async pattern:
1. Client initiates processing with POST → receives 202 Accepted + job ID
2. Client polls status endpoint GET `/process/{jobId}/` → receives progress
3. When complete, client retrieves results from GET `/insights/`

This prevents timeouts and improves user experience for long-running operations.

### 4. Flexible Querying
- **Pagination**: Prevents overwhelming clients with large datasets
- **Filtering**: Multiple operators (`contains`, `in`, `gte`, `lte`) for complex queries
- **Sorting**: Multi-field sorting with ascending/descending order
- **Combination**: All features work together for powerful queries

Example:
```
GET /books/?author__contains=tolkien&publicationDate__gte=1950-01-01&sort=-publicationDate,name&page=1&pageSize=10
```

### 5. Error Handling Strategy
- Consistent error response structure
- Field-level validation errors
- Descriptive error messages
- Appropriate HTTP status codes

### 6. API Versioning
- URL-based versioning (`/v1/`) for simplicity
- Allows breaking changes in future versions
- Easy to maintain multiple versions simultaneously

## Scalability Considerations

1. **Pagination**: Prevents memory issues with large result sets
2. **Async processing**: Allows horizontal scaling of processing workers
3. **Stateless design**: Enables load balancing across multiple servers
4. **Caching**: GET requests can be cached at various levels
5. **Job queuing**: Processing can be distributed across workers

## Security Considerations

1. **Authentication**: Bearer token required for all requests
2. **Authorization**: Can be implemented at resource level
3. **File validation**: Size limits and format checks prevent abuse
4. **Rate limiting**: Would be implemented to prevent DoS attacks
5. **Input validation**: All inputs are validated before processing

## Developer Experience

1. **Clear documentation**: Every endpoint fully documented
2. **Consistent patterns**: Similar operations follow same patterns
3. **Meaningful responses**: Rich response bodies with metadata
4. **Hypermedia links**: Related resources linked (HATEOAS principle)
5. **Predictable behavior**: Standard HTTP semantics

## Testing Strategy

This API design supports easy testing:
- **Unit tests**: Each endpoint can be tested independently
- **Integration tests**: Resource relationships can be verified
- **Load tests**: Pagination and async design support load testing
- **Mock responses**: Clear response structures enable mocking

## Implementation Notes

### Technology Stack Recommendations
- **Framework**: Django REST Framework (Python) or Express.js (Node.js)
- **Database**: PostgreSQL (excellent JSON support for insights)
- **File storage**: AWS S3 or similar object storage
- **Task queue**: Celery (Python) or Bull (Node.js) for async processing
- **Cache**: Redis for job status and frequent queries

### Database Schema Considerations
```sql
-- Books table
CREATE TABLE books (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publisher VARCHAR(255) NOT NULL,
    publication_date DATE NOT NULL,
    isbn VARCHAR(17) UNIQUE NOT NULL,
    cover_photo VARCHAR(2048),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Book contents table
CREATE TABLE book_contents (
    id UUID PRIMARY KEY,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    file_name VARCHAR(255),
    file_size INTEGER,
    content_type VARCHAR(100),
    storage_path VARCHAR(512),
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Processing jobs table
CREATE TABLE processing_jobs (
    id UUID PRIMARY KEY,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    status VARCHAR(20),
    progress INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

-- Insights table (stores JSON results)
CREATE TABLE book_insights (
    id UUID PRIMARY KEY,
    book_id UUID REFERENCES books(id) ON DELETE CASCADE,
    job_id UUID REFERENCES processing_jobs(id),
    insights JSONB,
    processed_at TIMESTAMP DEFAULT NOW()
);
```

## Comparison with Alternatives

### Why REST over GraphQL?
- **Simplicity**: REST is simpler for this use case
- **Caching**: Better HTTP caching support
- **Tooling**: More universal tooling support
- **Learning curve**: Easier for consumers

### Why Async Processing over Webhooks?
- **Reliability**: Polling is more reliable than webhooks
- **Simplicity**: No need for clients to expose endpoints
- **Flexibility**: Clients control polling frequency
- **Debugging**: Easier to debug and monitor

## Compliance & Standards

- **OpenAPI 3.0**: This design can be easily converted to OpenAPI spec
- **JSON:API**: Follows many JSON:API conventions
- **RFC 7231**: Proper HTTP semantics
- **ISO 8601**: Date/time format standard

---

This design balances simplicity with functionality, providing a robust API that can scale while remaining easy to use and maintain.
