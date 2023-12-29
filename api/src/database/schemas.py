"""
this file contains the database schemas for the endpoints or other function to handle incoming and outgoing data
"""

from __future__ import annotations

from typing import List
from pydantic import BaseModel


class ItemBase(BaseModel):
    """
    represents the base of an item.
    This class contains variables for every handled item.
    """
    labels: List[str] | None = None
    imageMetadata: dict | None = None


class ItemCreate(ItemBase):
    """
    represents the base item for creating a new item
    This class contains variables that are mandatory for creating an item
    """
    path: str
    sha256_digest: str
    pass


class ItemUpdate(ItemBase):
    """
    represents the base item for updating an item
    This class contains all the variables in the ItemBase
    """
    pass


class Item(ItemBase):
    """
    represents the base item returning from the database.
    This class contains all the variables saved inside the database. Use this class to return an item as response
    """
    path: str
    id: int
    sha256_digest: str
