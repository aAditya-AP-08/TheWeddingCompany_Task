# Design Notes - Organization Management Service

## Architecture Overview

This document explains the design choices, trade-offs, and architectural decisions made in building the Organization Management Service.

## Core Design Principles

### 1. Multi-Tenant Architecture Pattern

The system implements a **"Shared Database, Separate Collections"** multi-tenant pattern:

- **Master Database**: Stores global metadata (organizations, admin users)
- **Dynamic Collections**: Each organization gets its own MongoDB collection
- **Collection Naming**: `org_<normalized_organization_name>`

### 2. Class-Based Design

All business logic is encapsulated in service classes:
- `OrganizationService`: Handles all organization CRUD operations
- `AuthService`: Manages authentication and JWT token generation

This approach provides:
- **Testability**: Easy to mock and test individual components
- **Maintainability**: Clear separation of concerns
- **Reusability**: Services can be used across different API endpoints
- **Extensibility**: Easy to add new features without modifying existing code

## Database Design

### Master Database Collections

#### 1. `organizations` Collection
```json
{
  "_id": ObjectId,
  "organization_name": "Acme Corp",
  "collection_name": "org_acme_corp",
  "admin_user_id": ObjectId,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

**Indexes**:
- `organization_name` (unique) - Fast lookups
- `collection_name` (unique) - Prevent conflicts

#### 2. `admin_users` Collection
```json
{
  "_id": ObjectId,
  "email": "admin@acme.com",
  "password_hash": "$2b$12$...",
  "organization_name": "Acme Corp",
  "created_at": ISODate,
  "updated_at": ISODate
}
```

**Indexes**:
- `email` (unique) - Fast login lookups
- `organization_name` - For organization-based queries

### Dynamic Organization Collections

Each organization collection is created dynamically:
- **Naming Convention**: `org_<normalized_name>`
- **Normalization**: Lowercase, spaces replaced with underscores
- **Initialization**: Created with a basic schema document

## API Design

### RESTful Principles

- **POST** `/org/create` - Create resource
- **GET** `/org/get` - Read resource
- **PUT** `/org/update` - Update resource (idempotent)
- **DELETE** `/org/delete` - Delete resource
- **POST** `/admin/login` - Authentication action

### Request/Response Patterns

All endpoints use JSON request bodies (even GET) for consistency and extensibility. In production, GET endpoints could use query parameters.

## Security Design

### Password Security

- **Hashing**: bcrypt with automatic salt generation
- **Cost Factor**: Default (12 rounds)
- **Storage**: Never store plaintext passwords

### Authentication

- **JWT Tokens**: Stateless authentication
- **Token Payload**: Contains admin ID, email, and organization name
- **Expiration**: Configurable (default 30 minutes)
- **Algorithm**: HS256 (symmetric key)

### Authorization

- **Delete Endpoint**: Requires admin email verification
- **Update Endpoint**: Requires password verification
- **Future Enhancement**: Could use JWT token validation for all protected endpoints

## Data Migration Strategy

### Update Operation Flow

When an organization name is updated:

1. **Validation**: Verify admin credentials
2. **Data Migration**: 
   - Read all documents from old collection
   - Insert into new collection
   - Drop old collection
3. **Metadata Update**: Update master database records
4. **Atomicity**: Operations are sequential (could be enhanced with transactions)

**Trade-off**: Simple but not fully atomic. For production, consider:
- MongoDB transactions (requires replica set)
- Two-phase commit pattern
- Backup before migration

## Scalability Considerations

### Current Architecture Scalability

**Strengths**:
- ✅ Dynamic collections allow independent scaling per organization
- ✅ Async/await pattern supports high concurrency
- ✅ MongoDB horizontal scaling capabilities
- ✅ Stateless API design (easy to scale horizontally)

**Limitations**:
- ⚠️ Single database instance (can become bottleneck)
- ⚠️ No connection pooling optimization
- ⚠️ No caching layer
- ⚠️ Collection count grows linearly with organizations

### Scaling Strategies

#### Horizontal Scaling (Recommended)
1. **API Layer**: Deploy multiple FastAPI instances behind load balancer
2. **Database Layer**: MongoDB replica sets or sharding
3. **Caching**: Redis for frequently accessed organization metadata

#### Vertical Scaling
- Increase MongoDB instance resources
- Optimize indexes
- Connection pooling

#### Hybrid Approach (Best for Production)
- Separate databases for large organizations
- Shared database for small organizations
- Implement organization tiering

## Performance Optimizations

### Implemented
- Async/await for I/O operations
- Indexed lookups on organization_name and email
- Normalized collection names for fast access

### Future Enhancements
- **Connection Pooling**: Configure Motor connection pool size
- **Caching**: Redis cache for organization metadata
- **Lazy Loading**: Load organization collections on-demand
- **Batch Operations**: Support bulk operations for multiple organizations

## Error Handling

### Error Response Format
```json
{
  "detail": "Error message describing what went wrong"
}
```

### HTTP Status Codes
- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST (create)
- `400 Bad Request`: Validation errors, duplicate names
- `401 Unauthorized`: Authentication failures
- `404 Not Found`: Organization not found
- `500 Internal Server Error`: Server errors

## Testing Strategy

### Unit Testing (Recommended)
- Test service classes with mocked database
- Test authentication logic
- Test password hashing/verification

### Integration Testing (Recommended)
- Test API endpoints with test database
- Test data migration flows
- Test error scenarios

### Load Testing (Recommended)
- Test concurrent organization creation
- Test collection creation performance
- Test authentication performance

## Deployment Considerations

### Environment Configuration
- Use environment variables for all configuration
- Separate dev/staging/production configs
- Secure JWT secret key management

### Database Setup
- MongoDB replica set for production
- Automated backups
- Monitoring and alerting

### API Deployment
- Use production ASGI server (Gunicorn + Uvicorn workers)
- Enable HTTPS
- Implement rate limiting
- Add API versioning

## Alternative Architectures Considered

### 1. Separate Databases per Organization

**When to Use**:
- High security requirements
- Very large organizations
- Regulatory compliance needs

**Implementation**:
- Connection string per organization in master DB
- Dynamic connection management
- More complex but better isolation

### 2. Single Collection with Tenant ID

**When to Use**:
- Small number of organizations
- Need cross-organization queries
- Simple requirements

**Implementation**:
- Add `organization_id` field to all documents
- Single collection with compound indexes
- Simpler but less scalable

### 3. Hybrid Approach

**When to Use**:
- Mixed organization sizes
- Need flexibility

**Implementation**:
- Small orgs: Shared collections
- Large orgs: Separate databases
- Tier-based routing

## Conclusion

The current architecture balances:
- ✅ **Simplicity**: Easy to understand and maintain
- ✅ **Scalability**: Can handle growth with optimizations
- ✅ **Security**: Proper authentication and password handling
- ✅ **Flexibility**: Dynamic collections allow custom schemas

For production, consider:
1. Adding caching layer (Redis)
2. Implementing proper connection pooling
3. Adding comprehensive monitoring
4. Implementing backup and disaster recovery
5. Adding rate limiting and API versioning

