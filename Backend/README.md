# Organization Management Service

A multi-tenant backend service built with FastAPI and MongoDB for managing organizations with dynamic collection creation.

## Features

- ✅ Create organizations with dynamic MongoDB collections
- ✅ Get organization details
- ✅ Update organization (with data migration)
- ✅ Delete organization (authenticated admin only)
- ✅ Admin authentication with JWT tokens
- ✅ Secure password hashing with bcrypt
- ✅ Master database for global metadata
- ✅ Dynamic collection creation per organization

## Tech Stack

- **Framework**: FastAPI (Python 3.8+)
- **Database**: MongoDB (with Motor async driver)
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **Validation**: Pydantic

## Project Structure

```
PanduProject/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # MongoDB connection management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── organization.py     # Organization endpoints
│   │   └── auth.py             # Authentication endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── organization.py     # Organization data model
│   │   └── user.py             # Admin user data model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── organization.py     # Organization Pydantic schemas
│   │   └── auth.py             # Auth Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── organization_service.py  # Organization business logic
│   │   └── auth_service.py          # Authentication business logic
│   └── auth/
│       ├── __init__.py
│       ├── jwt_handler.py      # JWT token utilities
│       └── password.py         # Password hashing utilities
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PanduProject
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env file with your configuration
   # Update MONGODB_URL, JWT_SECRET_KEY, etc.
   ```

5. **Start MongoDB**
   ```bash
   # If using local MongoDB
   mongod
   
   # Or use MongoDB Atlas connection string in .env file
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

7. **Access API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Create Organization
**POST** `/org/create`

Request Body:
```json
{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "organization_name": "Acme Corp",
  "collection_name": "org_acme_corp",
  "admin_email": "admin@acme.com",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### 2. Get Organization
**GET** `/org/get`

Request Body:
```json
{
  "organization_name": "Acme Corp"
}
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "organization_name": "Acme Corp",
  "collection_name": "org_acme_corp",
  "admin_email": "admin@acme.com",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### 3. Update Organization
**PUT** `/org/update`

Request Body:
```json
{
  "current_organization_name": "Acme Corp",
  "new_organization_name": "Acme Corporation",
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "id": "507f1f77bcf86cd799439011",
  "organization_name": "Acme Corporation",
  "collection_name": "org_acme_corporation",
  "admin_email": "admin@acme.com",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T13:00:00"
}
```

### 4. Delete Organization
**DELETE** `/org/delete`

Request Body:
```json
{
  "organization_name": "Acme Corp",
  "email": "admin@acme.com"
}
```

Response:
```json
{
  "message": "Organization 'Acme Corp' deleted successfully"
}
```

### 5. Admin Login
**POST** `/admin/login`

Request Body:
```json
{
  "email": "admin@acme.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "organization_name": "Acme Corp",
  "admin_id": "507f1f77bcf86cd799439012"
}
```

## Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   API Layer  │  │ Service Layer│  │  Auth Layer  │     │
│  │              │  │              │  │              │     │
│  │ /org/create  │──│ Organization │──│   JWT +      │     │
│  │ /org/get     │  │   Service    │  │  Password   │     │
│  │ /org/update  │  │              │  │  Hashing    │     │
│  │ /org/delete  │  │              │  │              │     │
│  │ /admin/login │──│  Auth        │──│              │     │
│  └──────────────┘  │  Service     │  └──────────────┘     │
│                    └──────────────┘                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Database                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Master Database (org_master_db)            │    │
│  │                                                    │    │
│  │  ┌──────────────────┐  ┌──────────────────┐      │    │
│  │  │  organizations   │  │   admin_users    │      │    │
│  │  │  Collection      │  │   Collection     │      │    │
│  │  │                  │  │                  │      │    │
│  │  │ - org_name       │  │ - email          │      │    │
│  │  │ - collection_name│  │ - password_hash  │      │    │
│  │  │ - admin_user_id  │  │ - org_name       │      │    │
│  │  │ - created_at     │  │ - created_at     │      │    │
│  │  └──────────────────┘  └──────────────────┘      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Dynamic Organization Collections            │    │
│  │                                                    │    │
│  │  ┌──────────────┐  ┌──────────────┐              │    │
│  │  │ org_acme_corp│  │ org_xyz_inc  │  ...          │    │
│  │  │              │  │              │              │    │
│  │  │ - org data   │  │ - org data   │              │    │
│  │  │ - custom     │  │ - custom     │              │    │
│  │  │   fields     │  │   fields     │              │    │
│  │  └──────────────┘  └──────────────┘              │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Organization Creation Flow**:
   ```
   Client → POST /org/create → OrganizationService → 
   Validate → Create Admin User → Create Organization Record → 
   Create Dynamic Collection → Return Response
   ```

2. **Authentication Flow**:
   ```
   Client → POST /admin/login → AuthService → 
   Verify Credentials → Generate JWT → Return Token
   ```

3. **Update Flow**:
   ```
   Client → PUT /org/update → OrganizationService → 
   Verify Credentials → Migrate Data → Update Records → Return Response
   ```

## Design Choices & Architecture Analysis

### Strengths of Current Architecture

1. **Separation of Concerns**: Clear separation between API, service, and data layers
2. **Scalability**: Dynamic collections allow horizontal scaling per organization
3. **Security**: JWT authentication and bcrypt password hashing
4. **Flexibility**: Each organization can have its own schema/structure
5. **Async/Await**: FastAPI's async support for better performance

### Trade-offs & Considerations

#### Current Approach (Single Database, Multiple Collections)

**Pros**:
- Simpler deployment and management
- Easier cross-organization queries (if needed)
- Lower operational overhead
- Good for small to medium scale

**Cons**:
- All organizations share the same database instance
- Potential performance bottlenecks with many organizations
- Limited isolation between tenants
- Collection name conflicts possible (mitigated by normalization)

#### Alternative Architecture: Separate Databases per Organization

**Pros**:
- Complete data isolation
- Better performance isolation
- Easier to scale individual organizations
- Can move organizations to different servers

**Cons**:
- More complex connection management
- Higher operational overhead
- More difficult cross-organization operations
- Requires connection pooling strategy

#### Alternative Architecture: Single Collection with Tenant ID

**Pros**:
- Simplest schema
- Easy to query across organizations
- Single collection to manage

**Cons**:
- No data isolation
- Performance issues with large datasets
- Index management complexity
- Security concerns (data leakage risk)

### Recommended Improvements

1. **Connection Pooling**: Implement proper MongoDB connection pooling
2. **Caching**: Add Redis for frequently accessed organization metadata
3. **Rate Limiting**: Implement rate limiting per organization
4. **Audit Logging**: Add comprehensive audit logs for all operations
5. **Database Indexing**: Add indexes on frequently queried fields
6. **Migration Strategy**: Implement versioned migrations for organization collections
7. **Monitoring**: Add health checks and monitoring for collection health
8. **Backup Strategy**: Implement automated backups for organization collections

### Technology Stack Rationale

- **FastAPI**: Modern, fast, async-first framework with automatic API documentation
- **MongoDB**: Flexible schema, good for multi-tenant with dynamic collections
- **Motor**: Async MongoDB driver, perfect for FastAPI
- **JWT**: Stateless authentication, scalable
- **Pydantic**: Type-safe data validation and serialization

## Testing

Example API calls using curl:

```bash
# Create Organization
curl -X POST "http://localhost:8000/org/create" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Test Corp",
    "email": "admin@test.com",
    "password": "testpass123"
  }'

# Get Organization
curl -X GET "http://localhost:8000/org/get" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "Test Corp"
  }'

# Admin Login
curl -X POST "http://localhost:8000/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "testpass123"
  }'
```

## Environment Variables

Create a `.env` file with the following variables:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=org_master_db
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Organization Management Service
DEBUG=True
```

## License

This project is created for assignment purposes.

## Author

Backend Intern Assignment Submission

