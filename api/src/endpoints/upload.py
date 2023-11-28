"""
this file contains the /upload endpoints for the api
"""

from __future__ import annotations
import ast
from logging import getLogger

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session

from api.src.tools.FolderTools import FolderTools
from api.src.tools.MetadataTools import MetadataTools
from api.src.database import crud, schemas
from api.src.database.database import get_db


Logger = getLogger(__name__)
router = APIRouter()

allowed_content_type = ["jpeg", "jpg", "png"]


@router.post('/upload', response_model=schemas.Item, tags=["Upload Routes"])
async def upload_image(file: UploadFile, labels: str | None = None, db: Session = Depends(get_db)):
    """
    Upload an image file to the database. This is the main upload route. All incoming pictures will be processed here \f

    :param db: the database session
    :param file: the image to upload
    :param labels: the tags to add to the image as a list
    :return: a message if the file was saved or an error cure
    """

    if file.filename.split('.')[-1] not in allowed_content_type:
        raise HTTPException(status_code=400, detail={
            "message": "The file type is not supported",
            "file": file.filename,
            "content_type": file.content_type,
            "allowed_content_type": allowed_content_type})

    def save() -> str:
        # process the incoming file and save it according to the structure
        # replace underscores and spaces with dashes
        file.filename = file.filename.replace(" ", "-").replace("_", "-")
        # save the incoming file
        file.filename = FolderTools().getNextFilePosition() + file.filename
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        Logger.info("file saved: %s", file.filename)
        return file.filename

    # handle request if labels are used as parameter
    if labels is not None:
        try:
            string_list = ast.literal_eval(labels)

            if isinstance(string_list, list) and all(isinstance(item, str) for item in string_list):
                save()
                return crud.create_item(db, schemas.ItemCreate(
                    path=file.filename,
                    labels=string_list,
                    imageMetadata=MetadataTools.loadMetadataAsJson(file.filename)))
            raise HTTPException(status_code=400, detail={
                "message": "labels must be a list of stings formatted as a string",
                "labels": labels,
                "example": "[\"label1\", \"label2\"]"})
        except (SyntaxError, ValueError) as e:
            raise HTTPException(status_code=400, detail={
                "message": "labels must be a list of stings formatted as a string",
                "labels": labels,
                "example": "[\"label1\", \"label2\"]",
                "error": str(e)})
    # handle request if labels are not used as parameter
    else:
        save()
        return crud.create_item(db, schemas.ItemCreate(
            path=file.filename,
            labels=[],
            imageMetadata=MetadataTools.loadMetadataAsJson(file.filename)))
