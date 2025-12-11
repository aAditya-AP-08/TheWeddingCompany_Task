# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ MongoDB running locally or MongoDB Atlas account
- ✅ pip installed

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env file (use any text editor)
# Update these values:
# - MONGODB_URL (default: mongodb://localhost:27017)
# - JWT_SECRET_KEY (use a strong random string)
```

### 3. Start MongoDB

**Option A: Local MongoDB**
```bash
# Start MongoDB service
mongod
```

**Option B: MongoDB Atlas**
- Create free account at https://www.mongodb.com/cloud/atlas
- Create a cluster
- Get connection string
- Update `MONGODB_URL` in `.env` file

### 4. Run the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
```

### 5. Test the API

**Option A: Using Swagger UI**
1. Open browser: http://localhost:8000/docs
2. Try the endpoints interactively

**Option B: Using curl**
```bash
# Create organization
curl -X POST "http://localhost:8000/org/create" \
  -H "Content-Type: application/json" \
  -d '{"organization_name": "My Company", "email": "admin@mycompany.com", "password": "mypass123"}'

# Login
curl -X POST "http://localhost:8000/admin/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@mycompany.com", "password": "mypass123"}'
```

**Option C: Using test script**
```bash
# Make sure server is running, then:
python test_api.py
```

## Common Issues

### MongoDB Connection Error
- **Problem**: `Connection refused` or `Cannot connect to MongoDB`
- **Solution**: 
  - Ensure MongoDB is running (`mongod` or MongoDB service)
  - Check `MONGODB_URL` in `.env` file
  - For Atlas, ensure IP is whitelisted

### Port Already in Use
- **Problem**: `Address already in use`
- **Solution**: 
  - Change port: `uvicorn app.main:app --port 8001`
  - Or stop the process using port 8000

### Import Errors
- **Problem**: `ModuleNotFoundError`
- **Solution**: 
  - Ensure virtual environment is activated
  - Reinstall dependencies: `pip install -r requirements.txt`

### JWT Secret Key Warning
- **Problem**: Using default secret key
- **Solution**: 
  - Generate a secure key: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
  - Update `JWT_SECRET_KEY` in `.env`

## Next Steps

1. ✅ Verify all endpoints work using Swagger UI
2. ✅ Test with your own organization data
3. ✅ Review the architecture in `ARCHITECTURE.md`
4. ✅ Read design notes in `DESIGN_NOTES.md`

## API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

