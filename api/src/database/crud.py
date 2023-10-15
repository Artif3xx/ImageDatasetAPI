from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Item).offset(skip).limit(limit).all()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def get_items_by_label(db: Session, labels: list[str], skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Item).filter(models.Item.labels.contains(labels)).offset(skip).limit(limit).all()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def get_item_by_id(db: Session, item_id: int):
    try:
        item = db.get(models.Item, item_id)
        return item
    except Exception as e:
        return {"error": str(e)}


def create_item(db: Session, item: schemas.ItemCreate):
    try:
        db_item = models.Item(**item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    try:
        db_item = db.get(models.Item, item_id)
        db_item.labels = item.labels
        db_item.imageMetadata = item.imageMetadata
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def delete_item(db: Session, item: schemas.Item):
    try:
        db_item = db.get(models.Item, item.id)
        db.delete(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        return {"error": str(e)}
