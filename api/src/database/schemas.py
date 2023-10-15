from __future__ import annotations

from pydantic import BaseModel
from typing import List


class ItemBase(BaseModel):
    labels: List[str] | None = None
    imageMetadata: dict | None = None


class ItemCreate(ItemBase):
    path: str
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    path: str
    id: int
