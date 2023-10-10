from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
import random
import ast

from api.database import handler as db

router = APIRouter()


@router.get("/image")
async def getImageByID(imageID: int | None = None, path: str | None = None):
    """
    Get an image by the imageID. This simply returns the image as a file response. If you want to get the image info,
    you need to request the info endpoint. You need at least one parameter to get an image. If you pass both parameters,
    an error will be returned.

    :param imageID: the id of the image to search
    :param path: the path to the image file
    :return: the image with the given id
    """

    # check if the imageID and the path is None
    if imageID is None and path is None:
        return {"error": "you need to pass at least one parameter"}

    # check if the imageID and the path is not None. If this is the case, return an error
    if imageID is not None and path is not None:
        return {"error": "you can only pass one parameter to the constructor"}

    path: str
    # check if the imageID is not None and the path is None
    if imageID is not None and path is None:
        imageData = db.getImageByID(imageID)
        # check if an error occurred
        if "error" in imageData:
            return {"error": "id not found in the database"}
        else:
            path = imageData["path"]

    # check if the path is not None and the imageID is None
    if path is not None and imageID is None:
        imageData = db.getImageByPath(path)
        # check if an error occurred
        if "error" in imageData:
            return {"error": "path not found in the database"}
        else:
            path = imageData["path"]

    # check if the image exists
    if os.path.exists(path):
        # TODO: if a filepath is given but not existing, the server should handle this and update the database entry
        return FileResponse(path, headers={"Content-Type": "image/jpeg"})
    else:
        return {"error": "id not found in the database"}


@router.get("/image/random")
async def getImageRandom(labels: str | None = None):
    """
    Get a random image from the database. You can also pass a list of labels to get a random image with these labels.
    There must be at least one label inside a array. Example: ["label1", "label2"]. If you don´t want to search for
    images with the following label, you can simply ignore the parameter.

    :param labels: the labels to search for as list. Example: ["label1", "label2"]
    :return: the requested image as file response
    """
    if labels is None:
        maxID = db.getTableLength()
        useID = random.randint(1, maxID)
    else:
        if labels.startswith("[") and labels.endswith("]") or "\n" in labels:
            ids = {}
            try:
                if "\n" in labels:
                    labels: [str] = labels.split("\n")
                else:
                    labels = ast.literal_eval(labels)
            except ValueError:
                return {"error": "invalid label", "type": "ValueError"}
            finally:
                for item in labels:
                    if not isinstance(item, str):
                        return {"error": "invalid label", "type": "ValueError"}
                    else:
                        ids[item] = [i["id"] for i in db.getImagesWithLabel(item)]

                for item in ids:
                    ids[item] = set(ids[item])

                duplicates = list(set.intersection(*ids.values()))
                if len(duplicates) == 0:
                    return {"error": "no images found with these labels", "type": "ValueError"}
                useID = duplicates[random.randint(0, len(duplicates) - 1)]
        else:
            items = db.getImagesWithLabel(labels)
            ids = []
            for item in items:
                ids.append(item["id"])

            if len(ids) == 0:
                return {"error": "no images found with these labels", "type": "ValueError"}
            useID = ids[random.randint(0, len(ids) - 1)]
        # print(labels)

    image_path = db.getImageByID(useID)["path"]

    if os.path.exists(image_path):
        return FileResponse(image_path, headers={"Content-Type": "image/jpeg"})
    else:
        return {"error": "Bild nicht gefunden"}
