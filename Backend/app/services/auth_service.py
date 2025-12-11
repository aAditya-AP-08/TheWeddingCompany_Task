"""
Authentication service for admin login.
"""
from typing import Optional
from bson import ObjectId
from app.database import get_database
from app.models.user import AdminUser
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token
from fastapi import HTTPException, status


class AuthService:
    """Service class for authentication operations."""
    
    def __init__(self):
        self.db = get_database()
        self.users_collection = self.db["admin_users"]
    
    async def authenticate_admin(self, email: str, password: str) -> dict:
        """
        Authenticate admin user and return JWT token.
        
        Args:
            email: Admin email
            password: Admin password
            
        Returns:
            Dictionary with access token and user info
        """
        # Find admin user
        user_data = await self.users_collection.find_one({"email": email})
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(password, user_data["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create JWT token
        token_data = {
            "sub": str(user_data["_id"]),
            "email": user_data["email"],
            "organization_name": user_data["organization_name"]
        }
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "organization_name": user_data["organization_name"],
            "admin_id": str(user_data["_id"])
        }

