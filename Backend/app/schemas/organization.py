"""
Pydantic schemas for organization requests and responses.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    """Schema for creating an organization."""
    organization_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class OrganizationUpdate(BaseModel):
    """Schema for updating an organization."""
    current_organization_name: str = Field(..., min_length=1, max_length=100)
    new_organization_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class OrganizationGet(BaseModel):
    """Schema for getting an organization."""
    organization_name: str = Field(..., min_length=1)


class OrganizationDelete(BaseModel):
    """Schema for deleting an organization."""
    organization_name: str = Field(..., min_length=1)
    email: EmailStr


class OrganizationResponse(BaseModel):
    """Schema for organization response."""
    id: str
    organization_name: str
    collection_name: str
    admin_email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

