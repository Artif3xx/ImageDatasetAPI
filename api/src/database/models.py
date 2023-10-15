from sqlalchemy import Column, Integer, String, JSON, PickleType
from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "Images"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, index=True)
    imageMetadata = Column(JSON, index=True)
    labels = Column(PickleType, index=True)
