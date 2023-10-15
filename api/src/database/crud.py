from sqlalchemy.orm import Session

from . import models, schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.Item).offset(skip).limit(limit).all()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


def get_items_by_label(db: Session, labels: list[str], onlyOne: bool = False, skip: int = 0, limit: int = 100):
    try:
        items = []
        for item in db.query(models.Item).offset(skip).limit(limit).all():
            # if onlyOne is true, the item must have at least one of the labels
            if onlyOne:
                # iterate over the labels and check if the item has the label
                for label in labels:
                    # check if the label is in the items labels
                    if label in item.labels:
                        items.append(item)
                        # exit the inner loop when a match is found
                        break
            # if onlyOne is false, the item must have all the labels
            else:
                token = True
                for label in labels:
                    if label not in item.labels:
                        token = False
                        break
                if token:
                    items.append(item)

        return items

    except Exception as e:
        db.rollback()
        print(f"An error occurred: {str(e)}")
        return []


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
