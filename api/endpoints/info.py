from fastapi import APIRouter

from api.database import handler as db
from api.models import DatabaseEntry as cardModel

router = APIRouter()


@router.get("/imageInfo")
async def getImageInfoByID(imageID: int):
    imageData = db.getImageByID(imageID)
    model = cardModel.DatabaseEntry(imageData["path"], imageData["metadata"], imageData["labels"], imageData["id"])
    return model.getAsJson()


@router.get("/imageInfoByPath")
async def getImageInfoByPath(path: str):
    imageData = db.getImageByPath(path)
    model = cardModel.DatabaseEntry(imageData["path"], imageData["metadata"], imageData["labels"], imageData["id"])
    return model


@router.post("/updateImageInfo")
async def updateImageInfoByID(imageID: int, path: str, metadata: str, labels: str):
    return db.updateImageByID(imageID, path, metadata, labels)
