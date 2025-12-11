"""
User data models.
"""
from typing import Optional
from datetime import datetime
from bson import ObjectId


class AdminUser:
    """Admin user model stored in master database."""
    
    def __init__(
        self,
        email: str,
        password_hash: str,
        organization_name: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.email = email
        self.password_hash = password_hash
        self.organization_name = organization_name
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            "_id": self._id,
            "email": self.email,
            "password_hash": self.password_hash,
            "organization_name": self.organization_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "AdminUser":
        """Create user from dictionary."""
        return cls(
            _id=data.get("_id"),
            email=data["email"],
            password_hash=data["password_hash"],
            organization_name=data["organization_name"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

