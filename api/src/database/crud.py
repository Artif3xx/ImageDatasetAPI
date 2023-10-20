from __future__ import annotations

from sqlalchemy.orm import Session
from api.src.tools.FolderTools import FolderTools
from logging import getLogger

from . import models, schemas

Logger = getLogger(__name__)


def get_items(db: Session, skip: int = 0, limit: int | None = 100):
    """
    Get items from the database. This function is used to get all items from the database if the limit is set to None.
    If the limit is set to a number, the function will return the first n items from the database

    :param db: the database session, used to query the database
    :param skip: the number of items to skip before returning the items
    :param limit: the number of items to return, can be set to None to return all items
    :return: the requested items from the database
    """
    try:
        if limit is None:
            return db.query(models.Item).offset(skip).all()
        return db.query(models.Item).offset(skip).limit(limit).all()
    except Exception as e:
        db.rollback()
        Logger.error(f"error: {str(e)}")
        return {"error": str(e)}


def get_items_by_label(db: Session, labels: list[str], onlyOne: bool = False):
    """
    Get items from the database that have the specified labels. If onlyOne is set to True, the function will return
    all items that have at least one of the labels. If onlyOne is set to False, the function will return all items
    that have all the labels

    :param db: the database session, used to query the database
    :param labels: the labels to search for
    :param onlyOne: if set to True, the function will return all items that have at least one of the labels. If set to
        False, the function will return all items that have all the labels
    :return: the requested items from the database
    """
    try:
        label_set = set(labels)

        if onlyOne:
            # use any to return true if any label matches
            items = [item for item in db.query(models.Item).all() if any(label in item.labels for label in label_set)]
        else:
            # use all to return true only if all labels match
            items = [item for item in db.query(models.Item).all() if all(label in item.labels for label in label_set)]

        return items

    except Exception as e:
        db.rollback()
        Logger.error(f"error: {str(e)}")
        return []


def get_item_by_id(db: Session, item_id: int):
    """
    Get an item from the database by its id

    :param db: the database session, used to query the database
    :param item_id: the id of the item to get
    :return: the requested item from the database
    """
    try:
        item = db.get(models.Item, item_id)
        return item
    except Exception as e:
        Logger.error(f"error: {str(e)}")
        return {"error": str(e)}


def create_item(db: Session, item: schemas.ItemCreate):
    """
    Create an item in the database

    :param db: the database session, used to query the database
    :param item: the new item to create
    :return: the created item from the database
    """
    try:
        db_item = models.Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        FolderTools.deleteFile(item.path)
        Logger.error(f"error: {str(e)}")
        return {"error": str(e)}


def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    """
    Update an item in the database

    :param db: the database session, used to query the database
    :param item_id: the id of the item to update
    :param item: the new item to update
    :return: the updated item from the database
    """

    try:
        db_item = db.get(models.Item, item_id)
        db_item.labels = item.labels
        db_item.imageMetadata = item.imageMetadata
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        Logger.error(f"error: {str(e)}")
        return {"error": str(e)}


def delete_item(db: Session, item: schemas.Item):
    """
    Delete an item from the database

    :param db: the database session, used to query the database
    :param item: the item to delete
    :return: the deleted item from the database
    """
    try:
        db_item = db.get(models.Item, item.id)
        db.delete(db_item)
        db.commit()
        db.refresh(db_item)
        Logger.info(f"file deleted: {item.path}")
        return db_item
    except Exception as e:
        Logger.error(f"error: {str(e)}")
        return {"error": str(e)}
