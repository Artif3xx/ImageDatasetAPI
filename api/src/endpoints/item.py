from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException

from api.src.database import crud, schemas
from api.src.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/item/{item_id}", response_model=schemas.Item)
async def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    """
    Get an item by the itemID. This simply returns the item as a file response. If you want to get the item info,
    you need to request the info endpoint. You need at least one parameter to get an item. If you pass both parameters,
    an error will be returned.

    :param db:
    :param item_id: the id of the item to search
    :return: the item with the given id
    """
    item = crud.get_item_by_id(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return item


@router.post("/item/{item_id}/update", response_model=schemas.Item)
async def update_item_by_id(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Update the item for an item by itemID. The function can also be used to remove all item from an item by
    passing an empty list as item.

    :param db:
    :param item_id: the id of the item to update
    :param item: the new item
    :return: the updated item
    """
    if item.labels is None:
        raise HTTPException(status_code=400,
                            detail="Labels cannot be empty. There must be at least an empty list")

    if item.imageMetadata is None:
        raise HTTPException(status_code=400,
                            detail="ImageMetadata cannot be empty. There must be at least an empty dict")

    itemCheck = crud.get_item_by_id(db, item_id=item_id)
    if itemCheck is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

    return crud.update_item(db, item_id=item_id, item=item)


@router.delete("/item/{item_id}/delete", response_model=schemas.Item)
async def delete_item_by_id(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the item for an item by itemID.

    :param db:
    :param item_id: the id of the item to delete
    :return: the deleted item
    """
    itemCheck = crud.get_item_by_id(db, item_id=item_id)
    if itemCheck is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")

    return crud.delete_item(db, item=itemCheck)
