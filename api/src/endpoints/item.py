"""
this file contains the /item endpoints for the api
"""

from __future__ import annotations
import random

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.src.database import crud, schemas
from api.src.database.database import get_db

router = APIRouter()


@router.get("/items", response_model=list[schemas.Item], tags=["Item Routes"])
def read_items(skip: int = 0, limit: int | None = 100, db: Session = Depends(get_db)):
    """
    Get items from the database. You can leave all parameters and get all items from the database. You can also use
    the limite and skip parameters to get a subset of the items. The items are returned as a list of items. \f

    :param skip: the number of items to skip
    :param limit: the limit of items to return
    :param db: the database session to use
    :return: the items as a list
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/item/id/{item_id}", response_model=schemas.Item, tags=["Item Routes"])
async def get_item_by_id(item_id: int, db: Session = Depends(get_db)):
    """
    Get an item by the itemID. This simply returns the item as a file response. If you want to get the item info,
    you need to request the info endpoint. You need at least one parameter to get an item. If you pass both parameters,
    an error will be returned. \f

    :param db: the database session to use
    :param item_id: the id of the item to search
    :return: the item with the given id
    """
    if item_id == -1:
        return crud.get_last_item(db)
    if item_id == 0:
        return crud.get_first_item(db)
    item = crud.get_item_by_id(db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return item


@router.post("/item/id/{item_id}/update", response_model=schemas.Item, tags=["Item Routes"])
async def update_item_by_id(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Update the item for an item by itemID. The function can also be used to remove all item from an item by
    passing an empty list as item. \f

    :param db: the database session to use
    :param item_id: the id of the item to update
    :param item: the new item
    :return: the updated item
    """

    if item.labels is None and item.imageMetadata is None:
        raise HTTPException(status_code=400,
                            detail="Labels and ImageMetadata cannot be empty. There must be at least one empty list or dictionary")
    itemCheck = crud.get_item_by_id(db, item_id=item_id)
    if item.imageMetadata is None:
        item.imageMetadata = itemCheck.imageMetadata
    if item.labels is None:
        item.labels = itemCheck.labels
    if itemCheck is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return crud.update_item(db, item_id=item_id, item=item)


@router.delete("/item/id/{item_id}/delete", response_model=schemas.Item, tags=["Item Routes"])
async def delete_item_by_id(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the item for an item by itemID. \f

    :param db: the database session to use
    :param item_id: the id of the item to delete
    :return: the deleted item
    """
    itemCheck = crud.get_item_by_id(db, item_id=item_id)
    if itemCheck is None:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} not found")
    return crud.delete_item(db, item=itemCheck)


@router.get("/item/id/{item_id}/next", response_model=schemas.Item, tags=["Item Routes"])
async def get_next_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the next item after the item with the given id. If the item_id is 0, the first item will be returned. The id
    must be zero or positive. \f

    :param item_id: the id of the item to search
    :param db: the database session to use
    :return: the next item
    """
    if item_id == 0:
        return crud.get_first_item(db)
    if item_id < 0:
        raise HTTPException(status_code=404, detail=f"item_id '{item_id}' must be zero or positive")
    next_item = crud.get_next_item(db, current_id=item_id)
    if next_item is None:
        raise HTTPException(status_code=404, detail=f"There is nothing after item with id {item_id}!")
    return next_item


@router.get("/item/id/{item_id}/previous", response_model=schemas.Item, tags=["Item Routes"])
async def get_previous_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get the previous item before the item with the given id. If the item_id is -1, the last item will be returned. The
    id must be -1, 0 or another positive number. \f

    :param item_id: the id of the item to search
    :param db: the database session to use
    :return: the previous item
    """
    if item_id == -1:
        return crud.get_last_item(db)
    if item_id < 0:
        raise HTTPException(status_code=404, detail=f"Item with id {item_id} must be positive")
    previous_item = crud.get_previous_item(db, current_id=item_id)
    if previous_item is None:
        raise HTTPException(status_code=404, detail=f"There is nothing before item with id {item_id}!")
    return previous_item


@router.get("/item/random", response_model=schemas.Item, tags=["Item Routes"])
async def get_random_item(db: Session = Depends(get_db)):
    """
    Get a random item from the database. \f

    :param db: the database session to use
    :return: a random item
    """
    random_id = random.sample(crud.get_ids(db), 1)
    return crud.get_item_by_id(db, item_id=random_id)
