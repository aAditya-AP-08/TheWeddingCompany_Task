"""
Organization API routes.
"""
from fastapi import APIRouter, status
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationGet,
    OrganizationDelete,
    OrganizationResponse
)
from app.services.organization_service import OrganizationService

router = APIRouter(prefix="/org", tags=["organizations"])


@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate):
    """Create a new organization with admin user."""
    service = OrganizationService()
    result = await service.create_organization(
        organization_name=org_data.organization_name,
        email=org_data.email,
        password=org_data.password
    )
    return OrganizationResponse(**result)


@router.get("/get", response_model=OrganizationResponse)
async def get_organization(org_data: OrganizationGet):
    """Get organization by name."""
    service = OrganizationService()
    result = await service.get_organization(org_data.organization_name)
    return OrganizationResponse(**result)


@router.put("/update", response_model=OrganizationResponse)
async def update_organization(org_data: OrganizationUpdate):
    """Update organization name and migrate data."""
    service = OrganizationService()
    result = await service.update_organization(
        organization_name=org_data.current_organization_name,
        new_organization_name=org_data.new_organization_name,
        email=org_data.email,
        password=org_data.password
    )
    return OrganizationResponse(**result)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_organization(org_data: OrganizationDelete):
    """Delete organization (authenticated admin only)."""
    service = OrganizationService()
    result = await service.delete_organization(
        organization_name=org_data.organization_name,
        admin_email=org_data.email
    )
    return result

