# Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Applications                       │
│                    (Web, Mobile, API Clients)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/REST API
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application Layer                   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes (app/api/)                  │  │
│  │                                                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ Organization │  │   Auth API   │  │  Health      │  │  │
│  │  │    Routes    │  │    Routes    │  │  Check       │  │  │
│  │  │              │  │              │  │              │  │  │
│  │  │ POST /create │  │ POST /login  │  │ GET /health  │  │  │
│  │  │ GET /get     │  │              │  │              │  │  │
│  │  │ PUT /update  │  │              │  │              │  │  │
│  │  │ DELETE /del  │  │              │  │              │  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └──────────────┘  │  │
│  └─────────┼──────────────────┼────────────────────────────┘  │
│            │                  │                                 │
│            ▼                  ▼                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Service Layer (app/services/)                │  │
│  │                                                           │  │
│  │  ┌──────────────────┐      ┌──────────────────┐          │  │
│  │  │ Organization     │      │   Auth Service   │          │  │
│  │  │   Service        │      │                  │          │  │
│  │  │                  │      │ - Authenticate   │          │  │
│  │  │ - Create Org     │      │ - Generate JWT   │          │  │
│  │  │ - Get Org        │      │ - Verify Creds   │          │  │
│  │  │ - Update Org     │      │                  │          │  │
│  │  │ - Delete Org     │      │                  │          │  │
│  │  │ - Create Coll    │      │                  │          │  │
│  │  │ - Migrate Data   │      │                  │          │  │
│  │  └────────┬─────────┘      └────────┬─────────┘          │  │
│  └───────────┼──────────────────────────┼────────────────────┘  │
│              │                        │                          │
│              ▼                        ▼                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          Authentication & Security (app/auth/)            │  │
│  │                                                           │  │
│  │  ┌──────────────┐              ┌──────────────┐         │  │
│  │  │ JWT Handler  │              │  Password    │         │  │
│  │  │              │              │  Handler     │         │  │
│  │  │ - Create     │              │              │         │  │
│  │  │ - Verify     │              │ - Hash       │         │  │
│  │  │ - Decode     │              │ - Verify     │         │  │
│  │  └──────────────┘              └──────────────┘         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ Motor Async Driver
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MongoDB Database Layer                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Master Database: org_master_db                   │  │
│  │                                                           │  │
│  │  ┌────────────────────┐    ┌────────────────────┐      │  │
│  │  │  organizations     │    │   admin_users      │      │  │
│  │  │  Collection        │    │   Collection       │      │  │
│  │  │                    │    │                    │      │  │
│  │  │ • _id              │    │ • _id              │      │  │
│  │  │ • org_name         │    │ • email            │      │  │
│  │  │ • collection_name  │    │ • password_hash    │      │  │
│  │  │ • admin_user_id    │    │ • organization_name│      │  │
│  │  │ • timestamps       │    │ • timestamps       │      │  │
│  │  └────────────────────┘    └────────────────────┘      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Dynamic Organization Collections                  │  │
│  │                                                           │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │ org_acme_corp│  │ org_xyz_inc  │  │ org_test_ltd │  │  │
│  │  │              │  │              │  │              │  │  │
│  │  │ • Custom     │  │ • Custom     │  │ • Custom     │  │  │
│  │  │   Schema     │  │   Schema     │  │   Schema     │  │  │
│  │  │ • Org Data   │  │ • Org Data   │  │ • Org Data   │  │  │
│  │  │ • Documents  │  │ • Documents  │  │ • Documents  │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │                                                           │  │
│  │  ... (Created dynamically per organization) ...           │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Organization Creation Flow

```
┌─────────┐
│ Client  │
└────┬────┘
     │ POST /org/create
     │ {org_name, email, password}
     ▼
┌─────────────────┐
│ API Route       │ Validate Input
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Org Service     │ Check Duplicates
└────┬────────────┘
     │
     ├──► Check org_name exists? ──NO──┐
     │                                  │
     ├──► Check email exists? ──NO─────┤
     │                                  │
     ▼                                  │
┌─────────────────┐                    │
│ Hash Password   │                    │
└────┬────────────┘                    │
     │                                  │
     ▼                                  │
┌─────────────────┐                    │
│ Create Admin    │                    │
│ User Record     │                    │
└────┬────────────┘                    │
     │                                  │
     ▼                                  │
┌─────────────────┐                    │
│ Create Org      │                    │
│ Record          │                    │
└────┬────────────┘                    │
     │                                  │
     ▼                                  │
┌─────────────────┐                    │
│ Create Dynamic  │                    │
│ Collection      │                    │
└────┬────────────┘                    │
     │                                  │
     ▼                                  │
┌─────────────────┐                    │
│ Return Success  │                    │
│ Response        │                    │
└─────────────────┘                    │
     │                                  │
     └──────────────────────────────────┘
```

### Authentication Flow

```
┌─────────┐
│ Client  │
└────┬────┘
     │ POST /admin/login
     │ {email, password}
     ▼
┌─────────────────┐
│ Auth API        │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Auth Service    │
└────┬────────────┘
     │
     ├──► Find User by Email
     │
     ├──► User Found? ──NO──► Return 401
     │
     ├──► YES
     │
     ▼
┌─────────────────┐
│ Verify Password │
└────┬────────────┘
     │
     ├──► Password Valid? ──NO──► Return 401
     │
     ├──► YES
     │
     ▼
┌─────────────────┐
│ Generate JWT    │
│ Token           │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Return Token    │
│ + Org Info      │
└─────────────────┘
```

### Update Organization Flow (with Migration)

```
┌─────────┐
│ Client  │
└────┬────┘
     │ PUT /org/update
     │ {current_name, new_name, email, password}
     ▼
┌─────────────────┐
│ API Route       │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Org Service     │
└────┬────────────┘
     │
     ├──► Find Organization
     │
     ├──► Verify Admin Credentials
     │
     ├──► Check New Name Available
     │
     ▼
┌─────────────────┐
│ Read Old        │
│ Collection      │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Create New      │
│ Collection      │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Migrate Data    │
│ (Copy Docs)     │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Drop Old        │
│ Collection      │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Update Master   │
│ DB Records      │
└────┬────────────┘
     │
     ▼
┌─────────────────┐
│ Return Updated  │
│ Org Info        │
└─────────────────┘
```

## Component Responsibilities

### API Layer (`app/api/`)
- **Purpose**: Handle HTTP requests/responses
- **Responsibilities**:
  - Request validation (via Pydantic schemas)
  - Response formatting
  - HTTP status code management
  - Route definitions

### Service Layer (`app/services/`)
- **Purpose**: Business logic and orchestration
- **Responsibilities**:
  - Business rule enforcement
  - Data validation
  - Transaction coordination
  - Error handling

### Models (`app/models/`)
- **Purpose**: Data structure definitions
- **Responsibilities**:
  - Domain object representation
  - Data transformation (dict ↔ object)
  - Business entity modeling

### Schemas (`app/schemas/`)
- **Purpose**: API contract definition
- **Responsibilities**:
  - Request/response validation
  - Type safety
  - API documentation (OpenAPI)

### Auth Layer (`app/auth/`)
- **Purpose**: Security and authentication
- **Responsibilities**:
  - Password hashing/verification
  - JWT token generation/validation
  - Security utilities

### Database Layer (`app/database.py`)
- **Purpose**: Database connection management
- **Responsibilities**:
  - Connection lifecycle
  - Database access abstraction
  - Collection access helpers

