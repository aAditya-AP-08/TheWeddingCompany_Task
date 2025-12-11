"""
Organization data models.
"""
from typing import Optional
from datetime import datetime
from bson import ObjectId


class Organization:
    """Organization model stored in master database."""
    
    def __init__(
        self,
        organization_name: str,
        collection_name: str,
        admin_user_id: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        _id: Optional[ObjectId] = None
    ):
        self._id = _id or ObjectId()
        self.organization_name = organization_name
        self.collection_name = collection_name
        self.admin_user_id = admin_user_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert organization to dictionary."""
        return {
            "_id": self._id,
            "organization_name": self.organization_name,
            "collection_name": self.collection_name,
            "admin_user_id": self.admin_user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Organization":
        """Create organization from dictionary."""
        return cls(
            _id=data.get("_id"),
            organization_name=data["organization_name"],
            collection_name=data["collection_name"],
            admin_user_id=data["admin_user_id"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

