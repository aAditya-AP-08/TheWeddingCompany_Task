"""
Simple test script for API endpoints.
Run this after starting the server to test all endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

def test_create_organization():
    """Test creating an organization."""
    url = f"{BASE_URL}/org/create"
    data = {
        "organization_name": "Test Corp",
        "email": "admin@testcorp.com",
        "password": "testpass123"
    }
    response = requests.post(url, json=data)
    print_response("CREATE ORGANIZATION", response)
    return response.json() if response.status_code == 201 else None

def test_get_organization(org_name="Test Corp"):
    """Test getting an organization."""
    url = f"{BASE_URL}/org/get"
    data = {
        "organization_name": org_name
    }
    response = requests.get(url, json=data)
    print_response("GET ORGANIZATION", response)
    return response.json() if response.status_code == 200 else None

def test_admin_login(email="admin@testcorp.com", password="testpass123"):
    """Test admin login."""
    url = f"{BASE_URL}/admin/login"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=data)
    print_response("ADMIN LOGIN", response)
    return response.json() if response.status_code == 200 else None

def test_update_organization():
    """Test updating an organization."""
    url = f"{BASE_URL}/org/update"
    data = {
        "current_organization_name": "Test Corp",
        "new_organization_name": "Test Corporation",
        "email": "admin@testcorp.com",
        "password": "testpass123"
    }
    response = requests.put(url, json=data)
    print_response("UPDATE ORGANIZATION", response)
    return response.json() if response.status_code == 200 else None

def test_delete_organization(org_name="Test Corporation", email="admin@testcorp.com"):
    """Test deleting an organization."""
    url = f"{BASE_URL}/org/delete"
    data = {
        "organization_name": org_name,
        "email": email
    }
    response = requests.delete(url, json=data)
    print_response("DELETE ORGANIZATION", response)
    return response.json() if response.status_code == 200 else None

def test_health_check():
    """Test health check endpoint."""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    print_response("HEALTH CHECK", response)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("ORGANIZATION MANAGEMENT SERVICE - API TEST SUITE")
    print("="*60)
    
    # Test health check
    test_health_check()
    
    # Test create organization
    org_data = test_create_organization()
    
    if org_data:
        # Test get organization
        test_get_organization()
        
        # Test admin login
        login_data = test_admin_login()
        
        # Test update organization
        updated_org = test_update_organization()
        
        if updated_org:
            # Test get updated organization
            test_get_organization("Test Corporation")
        
        # Test delete organization
        test_delete_organization()
        
        # Verify deletion
        test_get_organization("Test Corporation")
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)

