"""
Authentication API routes.
"""
from fastapi import APIRouter, status
from app.schemas.auth import AdminLogin, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin", tags=["authentication"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def admin_login(login_data: AdminLogin):
    """Admin login endpoint."""
    service = AuthService()
    result = await service.authenticate_admin(
        email=login_data.email,
        password=login_data.password
    )
    return TokenResponse(**result)

