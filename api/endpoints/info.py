from __future__ import annotations

from fastapi import APIRouter
import json

from api.database import handler as db
from api.models import DatabaseEntry as cardModel

router = APIRouter()


@router.get("/info")
async def getImageInfoByID(imageID: int | None = None, path: str | None = None):
    """
    Get the image info by the imageID or the path. You can also use both, but they have to match. If no query
    parameter is used, the package.json file will be returned.

    :param imageID: the id of the image
    :param path: the path of the image
    :return: the info as a json string
    """
    # check if imageID or path is None and return a basic info
    if imageID is None and path is None:
        info = json.load(open("package.json"))
        return {"info": info}

    # check if the imageID and the path is not None. If so, check if they match and return the info
    if imageID is not None and path is not None:
        imageData1 = db.getImageByID(imageID)
        imageData2 = db.getImageByPath(path)

        if imageData1 == imageData2:
            # check if the image data is an error
            if "error" in imageData1 or "error" in imageData2:
                return imageData1
            model = cardModel.DatabaseEntry(imageData1["path"], imageData1["metadata"], imageData1["labels"], imageData1["id"])
            return model.asJson()

        return {"error": "imageID and path do not match"}

    # check if the imageID is not None, but the path is. If so, process only the imageID
    if imageID is not None and path is None:
        imageData = db.getImageByID(imageID)
        # check if the image data is an error
        if "error" in imageData:
            return imageData
        model = cardModel.DatabaseEntry(imageData["path"], imageData["metadata"], imageData["labels"], imageData["id"])
        return model.asJson()

    # check if the path is not None, but the imageID is. If so, process only the path
    if path is not None and imageID is None:
        imageData = db.getImageByPath(path)
        # check if the image data is an error
        if "error" in imageData:
            return imageData
        model = cardModel.DatabaseEntry(imageData["path"], imageData["metadata"], imageData["labels"], imageData["id"])
        return model.asJson()


@router.post("/info/update")
async def updateImageInfoByID(imageID: int, metadata: str | None, labels: str| None):
    """
    Update the image info by the imageID. You can also use both, but they have to match.

    :param imageID: the image id to update
    :param metadata: the new metadata as a dictionary as a string
    :param labels: the new labels as a list with strings as a string
    :return: a message if the update was successful
    """
    # check if metadata and labels are None and return an error
    if metadata is None and labels is None:
        return {"error": "metadata and labels are None. What do you want to update?"}

    # check if metadata and labels are not None and update them
    if metadata is not None and labels is not None:
        if not metadata.startswith("{") or not metadata.endswith("}"):
            # TODO: check if the metadata is a dictionary as a string
            return {"error": "metadata is not a dictionary"}

        if not labels.startswith("[") or not labels.endswith("]"):
            # TODO: check if the labels are a list with strings as a string
            return {"error": "labels is not a list. Example: [\"label1\", \"label2\"]"}

        imageData = db.getImageByID(imageID)
        return db.updateImageByID(imageID, imageData["path"], metadata, labels)

    # check if the metadata is not None but the labels is and update the metadata
    if metadata is not None and labels is None:
        if not metadata.startswith("{") or not metadata.endswith("}"):
            # TODO: check if the metadata is a dictionary as a string
            return {"error": "metadata is not a dictionary"}

        imageData = db.getImageByID(imageID)
        return db.updateImageByID(imageID, imageData["path"], metadata, imageData["labels"])

    # check if the labels is not None but the metadata is and update the labels
    if metadata is None and labels is not None:
        if not labels.startswith("[") or not labels.endswith("]"):
            return {"error": "labels is not a list. Example: [\"label1\", \"label2\"]"}

        imageData = db.getImageByID(imageID)
        return db.updateImageByID(imageID, imageData["path"], imageData["metadata"], labels)
