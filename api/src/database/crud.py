"""
Crud repository of the projects. All the database related functions are located here.
crud stands for c - create, r - request, u - update and d - delete.
"""

from __future__ import annotations

import collections
from logging import getLogger
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError

from api.src.tools.FolderTools import FolderTools
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
    except IntegrityError as e:
        db.rollback()
        Logger.error("IntegrityError: %s", str(e))
        return {"error": "IntegrityError: " + str(e)}
    except DataError as e:
        db.rollback()
        Logger.error("DataError: %s", str(e))
        return {"error": "DataError: " + str(e)}
    except SQLAlchemyError as e:
        db.rollback()
        Logger.error("SQLAlchemyError: %s", str(e))
        return {"error": "SQLAlchemyError: " + str(e)}


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
    except IntegrityError as e:
        db.rollback()
        Logger.error("IntegrityError: %s", str(e))
        return {"error": "IntegrityError: " + str(e)}
    except DataError as e:
        db.rollback()
        Logger.error("DataError: %s", str(e))
        return {"error": "DataError: " + str(e)}
    except SQLAlchemyError as e:
        db.rollback()
        Logger.error("SQLAlchemyError: %s", str(e))
        return {"error": "SQLAlchemyError: " + str(e)}


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
    except IntegrityError as e:
        db.rollback()
        Logger.error("IntegrityError: %s", str(e))
        return {"error": "IntegrityError: " + str(e)}
    except DataError as e:
        db.rollback()
        Logger.error("DataError: %s", str(e))
        return {"error": "DataError: " + str(e)}
    except SQLAlchemyError as e:
        db.rollback()
        Logger.error("SQLAlchemyError: %s", str(e))
        return {"error": "SQLAlchemyError: " + str(e)}


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
    except IntegrityError as e:
        db.rollback()
        FolderTools.deleteFile(item.path)
        Logger.error("IntegrityError: %s", str(e))
        return {"error": "IntegrityError: " + str(e)}
    except DataError as e:
        db.rollback()
        FolderTools.deleteFile(item.path)
        Logger.error("DataError: %s", str(e))
        return {"error": "DataError: " + str(e)}
    except SQLAlchemyError as e:
        db.rollback()
        FolderTools.deleteFile(item.path)
        Logger.error("SQLAlchemyError: %s", str(e))
        return {"error": "SQLAlchemyError: " + str(e)}


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
    except IntegrityError as e:
        db.rollback()
        Logger.error("IntegrityError: %s", str(e))
        return {"error": "IntegrityError: " + str(e)}
    except DataError as e:
        db.rollback()
        Logger.error("DataError: %s", str(e))
        return {"error": "DataError: " + str(e)}
    except SQLAlchemyError as e:
        db.rollback()
        Logger.error("SQLAlchemyError: %s", str(e))
        return {"error": "SQLAlchemyError: " + str(e)}


def delete_item(db: Session, item: schemas.Item):
    """
    Delete an item from the database

    :param db: the database session, used to query the database
    :param item: the item to delete
    :return: the deleted item from the database
    """

    try:
        image_filepath: str = item.path
        db_item = db.get(models.Item, item.id)
        db.delete(db_item)
        db.commit()
        FolderTools.deleteFile(filepath=image_filepath)
        Logger.info("file deleted: %s", image_filepath)
        return db_item
    except IntegrityError as e:
        db.rollback()
        Logger.error("IntegrityError: %s", str(e))
        return {"error": "IntegrityError: " + str(e)}
    except DataError as e:
        db.rollback()
        Logger.error("DataError: %s", str(e))
        return {"error": "DataError: " + str(e)}
    except SQLAlchemyError as e:
        db.rollback()
        Logger.error("SQLAlchemyError: %s", str(e))
        return {"error": "SQLAlchemyError: " + str(e)}


def get_next_item(db: Session, current_id: int):
    """
    get the next item from the database by an id

    :param db: the database session, used to query the database
    :param current_id: the id to start the search from
    :return: the next item from the database
    """
    next_item = db.query(models.Item).filter(models.Item.id > current_id).first()
    return next_item if next_item else None


def get_previous_item(db: Session, current_id: int):
    """
    get the previous item from the database by an id

    :param db: the database session, used to query the database
    :param current_id: the id to start the search from
    :return: the previous item from the database
    """
    previous_item = db.query(models.Item).filter(models.Item.id < current_id).order_by(models.Item.id.desc()).first()
    return previous_item if previous_item else None


def get_last_item(db: Session):
    """
    get the last item from the database

    :param db: the database session, used to query the database
    :return: the last item from the database
    """
    last_item = db.query(models.Item).order_by(models.Item.id.desc()).first()
    return last_item if last_item else None


def get_first_item(db: Session):
    """
    get the first item from the database

    :param db: the database session, used to query the database
    :return: the first item from the database
    """
    last_item = db.query(models.Item).order_by(models.Item.id).first()
    return last_item if last_item else None


def get_labels(db: Session):
    """
    get all labels from the database

    :param db: the database session, used to query the database
    :return: all available labels from the database
    """
    item_labels = db.query(models.Item.labels).all()
    # item_labels = [[['labels 1', 'label2']], [['labels 1', 'label2']]]
    all_labels = {}
    for labels in item_labels:
        for label in labels[0]:
            if label not in all_labels:
                all_labels[label] = {'count': 1}
            else:
                all_labels[label]['count'] += 1
    return all_labels


def get_ids(db: Session):
    """
    get all ids from the database

    :param db: the database session, used to query the database
    :return: all available ids from the database
    """
    item_ids = db.query(models.Item.id).all()
    return [int(i[0]) for i in item_ids]
