"""
Database connection and utilities for MongoDB.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings
from typing import Optional


class Database:
    """Database connection manager."""
    
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


db = Database()


async def connect_to_mongo():
    """Create database connection."""
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.mongodb_db_name]
    print(f"Connected to MongoDB: {settings.mongodb_db_name}")


async def close_mongo_connection():
    """Close database connection."""
    if db.client:
        db.client.close()
        print("Disconnected from MongoDB")


def get_database() -> AsyncIOMotorDatabase:
    """Get the master database instance."""
    return db.database


def get_organization_collection(organization_name: str):
    """Get a dynamic collection for a specific organization."""
    collection_name = f"org_{organization_name.lower().replace(' ', '_')}"
    return db.database[collection_name]

