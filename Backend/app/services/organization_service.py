"""
Organization service for managing organizations and dynamic collections.
"""
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.database import get_database, get_organization_collection
from app.models.organization import Organization
from app.models.user import AdminUser
from app.auth.password import hash_password, verify_password
from fastapi import HTTPException, status


class OrganizationService:
    """Service class for organization operations."""
    
    def __init__(self):
        self.db = get_database()
        self.orgs_collection = self.db["organizations"]
        self.users_collection = self.db["admin_users"]
    
    async def create_organization(
        self,
        organization_name: str,
        email: str,
        password: str
    ) -> dict:
        """
        Create a new organization with admin user and dynamic collection.
        
        Args:
            organization_name: Name of the organization
            email: Admin email
            password: Admin password
            
        Returns:
            Organization metadata dictionary
        """
        # Normalize organization name for collection name
        normalized_name = organization_name.lower().replace(' ', '_')
        collection_name = f"org_{normalized_name}"
        
        # Check if organization already exists
        existing_org = await self.orgs_collection.find_one(
            {"organization_name": organization_name}
        )
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Organization '{organization_name}' already exists"
            )
        
        # Check if email already exists
        existing_user = await self.users_collection.find_one({"email": email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{email}' is already registered"
            )
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create admin user
        admin_user = AdminUser(
            email=email,
            password_hash=password_hash,
            organization_name=organization_name
        )
        user_result = await self.users_collection.insert_one(admin_user.to_dict())
        admin_user_id = str(user_result.inserted_id)
        
        # Create organization
        organization = Organization(
            organization_name=organization_name,
            collection_name=collection_name,
            admin_user_id=admin_user_id
        )
        org_result = await self.orgs_collection.insert_one(organization.to_dict())
        
        # Create dynamic collection for the organization
        org_collection = get_organization_collection(organization_name)
        # Initialize with a basic schema/document
        await org_collection.insert_one({
            "organization_name": organization_name,
            "created_at": datetime.utcnow(),
            "initialized": True
        })
        
        return {
            "id": str(org_result.inserted_id),
            "organization_name": organization_name,
            "collection_name": collection_name,
            "admin_email": email,
            "created_at": organization.created_at,
            "updated_at": organization.updated_at
        }
    
    async def get_organization(self, organization_name: str) -> dict:
        """
        Get organization by name.
        
        Args:
            organization_name: Name of the organization
            
        Returns:
            Organization metadata dictionary
        """
        org_data = await self.orgs_collection.find_one(
            {"organization_name": organization_name}
        )
        
        if not org_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{organization_name}' not found"
            )
        
        # Get admin user details
        admin_user = await self.users_collection.find_one(
            {"_id": ObjectId(org_data["admin_user_id"])}
        )
        
        return {
            "id": str(org_data["_id"]),
            "organization_name": org_data["organization_name"],
            "collection_name": org_data["collection_name"],
            "admin_email": admin_user["email"] if admin_user else "N/A",
            "created_at": org_data["created_at"],
            "updated_at": org_data["updated_at"]
        }
    
    async def update_organization(
        self,
        organization_name: str,
        new_organization_name: str,
        email: str,
        password: str
    ) -> dict:
        """
        Update organization name and migrate data to new collection.
        
        Args:
            organization_name: Current organization name
            new_organization_name: New organization name
            email: Admin email
            password: Admin password
            
        Returns:
            Updated organization metadata dictionary
        """
        # Get existing organization
        org_data = await self.orgs_collection.find_one(
            {"organization_name": organization_name}
        )
        
        if not org_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{organization_name}' not found"
            )
        
        # Check if new name already exists (if different)
        if new_organization_name != organization_name:
            existing_org = await self.orgs_collection.find_one(
                {"organization_name": new_organization_name}
            )
            if existing_org:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Organization '{new_organization_name}' already exists"
                )
        
        # Verify admin credentials
        admin_user = await self.users_collection.find_one(
            {"_id": ObjectId(org_data["admin_user_id"])}
        )
        
        if not admin_user or admin_user["email"] != email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin credentials"
            )
        
        if not verify_password(password, admin_user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid admin credentials"
            )
        
        # Handle collection migration only if organization name changes
        if new_organization_name != organization_name:
            # Get old collection
            old_collection = get_organization_collection(organization_name)
            
            # Create new collection name
            new_normalized_name = new_organization_name.lower().replace(' ', '_')
            new_collection_name = f"org_{new_normalized_name}"
            new_collection = get_organization_collection(new_organization_name)
            
            # Migrate data from old collection to new collection
            old_documents = await old_collection.find({}).to_list(length=None)
            if old_documents:
                # Remove _id fields for re-insertion
                for doc in old_documents:
                    doc.pop("_id", None)
                await new_collection.insert_many(old_documents)
            
            # Delete old collection
            await old_collection.drop()
        else:
            # Name hasn't changed, use existing collection name
            new_collection_name = org_data["collection_name"]
        
        # Update organization in master database
        update_data = {
            "organization_name": new_organization_name,
            "collection_name": new_collection_name,
            "updated_at": datetime.utcnow()
        }
        
        await self.orgs_collection.update_one(
            {"_id": org_data["_id"]},
            {"$set": update_data}
        )
        
        # Update admin user
        await self.users_collection.update_one(
            {"_id": ObjectId(org_data["admin_user_id"])},
            {
                "$set": {
                    "organization_name": new_organization_name,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        return {
            "id": str(org_data["_id"]),
            "organization_name": new_organization_name,
            "collection_name": new_collection_name,
            "admin_email": email,
            "created_at": org_data["created_at"],
            "updated_at": update_data["updated_at"]
        }
    
    async def delete_organization(
        self,
        organization_name: str,
        admin_email: str
    ) -> dict:
        """
        Delete organization and its collection.
        
        Args:
            organization_name: Name of the organization
            admin_email: Admin email for verification
            
        Returns:
            Success message
        """
        # Get organization
        org_data = await self.orgs_collection.find_one(
            {"organization_name": organization_name}
        )
        
        if not org_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Organization '{organization_name}' not found"
            )
        
        # Verify admin user
        admin_user = await self.users_collection.find_one(
            {"_id": ObjectId(org_data["admin_user_id"])}
        )
        
        if not admin_user or admin_user["email"] != admin_email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized: Only the organization admin can delete"
            )
        
        # Delete organization collection
        org_collection = get_organization_collection(organization_name)
        await org_collection.drop()
        
        # Delete admin user
        await self.users_collection.delete_one({"_id": ObjectId(org_data["admin_user_id"])})
        
        # Delete organization from master database
        await self.orgs_collection.delete_one({"_id": org_data["_id"]})
        
        return {
            "message": f"Organization '{organization_name}' deleted successfully"
        }

