"""
This file contains the endpoints for images. This is the best way to get images to process. Images will be responded
as FileResponse. Look inside the /example folder for more information about the usage
"""

from __future__ import annotations
import os
import random

from io import BytesIO
import numpy as np
from PIL import Image

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, Response

from api.src.database import crud
from api.src.database.database import get_db


router = APIRouter()

# valid modes for the orientation parameter
valid_orientations = ["landscape", "portrait", "square"]


@router.get("/image/id/{image_id}", tags=["image routes"])
async def get_image_by_id(image_id: int, db=Depends(get_db), width: int | None = None, orientation: str | None = None):
    """
    Get an image by the imageID. This simply returns the image as a file response. If you want to get the image info,
    you need to request the info endpoint. You need at least one parameter to get an image. If you pass both parameters,
    an error will be returned.

    :param db: the database session to use
    :param image_id: the id of the image to request
    :param width: the width of the image. If you pass this parameter, the image will be resized to the given width
    :param orientation: how the image should be oriented. Possible values are: "landscape", "portrait" and "square"
    :return: the image with the given id
    """

    filepath = ""
    # check if the imageID is not None and the path is None
    if image_id is not None:
        imageData = crud.get_item_by_id(db, item_id=image_id)
        # check if an error occurred
        if imageData is None:
            raise HTTPException(status_code=400, detail={"error": "id not found in the database"})
        filepath = imageData.path

    # check if the image exists
    if not os.path.exists(filepath):
        raise HTTPException(status_code=400, detail={"error": "file not found in the filesystem"})

    # ----------------------------------------------------------------------------------------------------
    # check if an orientations or a width is passed as parameter
    if orientation or width:
        image = Image.open(filepath)
        # handle the orientation parameter
        if orientation:
            if orientation not in valid_orientations:
                raise HTTPException(status_code=400, detail={"error": "invalid orientation parameter",
                                                             "valid orientations": valid_orientations})
            if orientation == "landscape":
                if image.height > image.width:
                    image = image.rotate(-90, expand=True)
            elif orientation == "portrait":
                if image.height < image.width:
                    image = image.rotate(-90, expand=True)
            elif orientation == "square":
                if width is None:
                    raise HTTPException(status_code=400, detail={"error": "width parameter is required "
                                                                          "when using square orientation"})
                image = image.resize((width, width))
                return Response(content=image_as_bytes(image),
                                headers={"Content-Type": "image/jpeg"}, media_type="image/jpeg")

        # handle the width parameter
        if width:
            old_dimension_ratio = width / image.width
            new_height = int(image.height * old_dimension_ratio)
            image = image.resize((width, new_height))
        return Response(content=image_as_bytes(image),
                        headers={"Content-Type": "image/jpeg"}, media_type="image/jpeg")
    # ----------------------------------------------------------------------------------------------------
    return FileResponse(filepath, headers={"Content-Type": "image/jpeg"})


def image_as_bytes(src_image: Image) -> bytes:
    """
    Convert a numpy array to bytes. This is used to return the image as a file response

    :param src_image: the image as numpy array
    :return: the image as bytes
    """
    image_pil = src_image

    with BytesIO() as buffer:
        image_pil.save(buffer, format="JPEG")
        image_bytes = buffer.getvalue()

        return image_bytes


@router.get("/image/random", tags=["image routes"])
async def get_random_image(labels: str | None = None, db=Depends(get_db)):
    """
    Get a random image from the database. You can also pass a list of labels to get a random image with these labels.
    There must be at least one label inside an array. Example: ["label1", "label2"]. If you don´t want to search for
    images with the following label, you can simply ignore the parameter.

    :param labels: the labels to search for as list. Example: ["label1", "label2"]
    :param db: the database session to use
    :return: the requested image as file response
    """

    random_id = random.sample(crud.get_ids(db), 1)
    imageData = crud.get_item_by_id(db, item_id=random_id)
    return FileResponse(imageData.path, headers={"Content-Type": "image/jpeg"})
