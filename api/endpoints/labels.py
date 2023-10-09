from __future__ import annotations

from fastapi import APIRouter
import ast

from api.database import handler as db
from api.models import DatabaseEntry as cardModel

router = APIRouter()


@router.get("/labels")
async def getLabels(imageID: int | None = None, path: str | None = None):
    """
    Get the available labels for an image by imageID or path. You can use both but in the database they must match. If
    no query parameter is used, all available labels are returned.

    :param imageID: the id of the image to search
    :param path: the path of the image to search
    :return: the labels for the image if available
    """
    # check if both imageID and path are None and return a basic info
    if imageID is None and path is None:
        return {"msg": "please provide an imageID or a path"}

    # check if imageID and path are not None, compare if both items are the same and return the labels
    if imageID is not None and path is not None:
        imageData1 = db.getImageByID(imageID)
        imageData2 = db.getImageByPath(path)

        if imageData1 == imageData2:
            # check if the image data is an error
            if "error" in imageData1 or "error" in imageData2:
                return imageData1
            model = cardModel.DatabaseEntry(imageData1["path"], imageData1["metadata"], imageData1["labels"],
                                            imageData1["id"])
            return model.getLabels()

        return {"error": "imageID and path do not match"}

    # check if the imageID is not None but the path is and return the labels for the path
    if imageID is not None and path is None:
        imageData = db.getImageByID(imageID)
        model = cardModel.DatabaseEntry(imageData["path"], imageData["metadata"], imageData["labels"], imageData["id"])
        return model.getLabels()

    # check if the path is not None but the imageID is and return the labels for the path
    if path is not None and imageID is None:
        imageData = db.getImageByPath(path)
        model = cardModel.DatabaseEntry(imageData["path"], imageData["metadata"], imageData["labels"], imageData["id"])
        return model.getLabels()


@router.post("/labels/update")
async def updateLabelsByID(imageID: int, labels: str):
    """
    Update the labels for an image by imageID. The function can also be used to remove all labels from an image by
    passing an empty list as labels.

    :param imageID: the id of the image to update
    :param labels: the labels to set for the image. Example: ["label1", "label2"]
    :return: a message if the update was successful
    """
    if not labels.startswith("[") or not labels.endswith("]"):
        return {"error": "labels is not a list. Example: [\"label1\", \"label2\"]"}

    # TODO: check if the labels are a list with strings as a string or damaged
    labels = labels.replace("\"", "'")
    return db.updateImageLabelsByID(imageID, labels)


@router.get("/labels/search")
async def getImageIDsWithLabel(labels: str):
    """
    Get all imageIDs that have the given labels. The labels must be passed as a list. Example: ["label1", "label2"] You
    need at least one label to search for. If you want to search for multiple labels, you can pass them as a list.

    :param labels: the labels to search for. Example: ["label1", "label2"]
    :return: the imageIDs that have the given labels
    """
    if not labels.startswith("[") and labels.endswith("]"):
        return {"error": "labels is not a list. At least one element is necessary! Example: [\"label1\", \"label2\"]"}

    try:
        # TODO: check if the labels are a list with strings as a string or damaged
        labels = ast.literal_eval(labels)
    except ValueError:
        return {"error": "invalid label", "type": "ValueError"}
    finally:
        ids = {}
        for label in labels:
            if not isinstance(label, str):
                return {"error": "labels is not a list. Example: [\"label1\", \"label2\"]"}
            else:
                images = db.getImagesWithLabel(label)
                if "error" in images:
                    continue

                ids[label] = [i["id"] for i in images]

        for item in ids:
            ids[item] = set(ids[item])

        # get the duplicate elements in all arrays. This indicates that the images have all labels
        duplicateIDs = set.intersection(*ids.values())
        return {"imageIDs": list(duplicateIDs), "labels": labels}
