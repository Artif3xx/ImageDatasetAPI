from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import os

from api.src.database import crud
from api.src.database.database import get_db

router = APIRouter()


@router.get("/image/{image_id}")
async def getImageByID(image_id: int, db=Depends(get_db)):
    """
    Get an image by the imageID. This simply returns the image as a file response. If you want to get the image info,
    you need to request the info endpoint. You need at least one parameter to get an image. If you pass both parameters,
    an error will be returned.

    :param db:
    :param image_id: the id of the image to search
    :return: the image with the given id
    """

    filepath = ""
    # check if the imageID is not None and the path is None
    if image_id is not None:
        imageData = crud.get_item_by_id(db, item_id=image_id)
        # check if an error occurred
        if imageData is None:
            raise HTTPException(status_code=400, detail={"error": "id not found in the database"})
        else:
            filepath = imageData.path

    # check if the image exists
    if os.path.exists(filepath):
        # TODO: if a filepath is given but not existing, the server should handle this and update the database entry
        return FileResponse(filepath, headers={"Content-Type": "image/jpeg"})
    else:
        raise HTTPException(status_code=400, detail={"error": "file not found in the filesystem"})


@router.get("/image/random")
async def getImageRandom(labels: str | None = None):
    """
    Get a random image from the database. You can also pass a list of labels to get a random image with these labels.
    There must be at least one label inside a array. Example: ["label1", "label2"]. If you don´t want to search for
    images with the following label, you can simply ignore the parameter.

    :param labels: the labels to search for as list. Example: ["label1", "label2"]
    :return: the requested image as file response
    """

    return {"msg": "random image"}
