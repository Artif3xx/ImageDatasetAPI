"""
This file holds the base item from the database.
"""
from sqlalchemy import Column, Integer, String, JSON, PickleType

from .database import Base


class Item(Base):
    """
    base item from the database.
    """
    __tablename__ = "Images"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    imageMetadata = Column(JSON, index=True)
    labels = Column(PickleType, index=True)
    sha256_digest = Column(String, index=True)
