from __future__ import annotations

from fastapi import APIRouter, UploadFile, Depends, HTTPException
from api.src.tools.FolderTools import FolderTools

from api.src.database import crud, schemas
from api.src.database.database import get_db
from sqlalchemy.orm import Session

import ast

router = APIRouter()


@router.post('/upload', response_model=schemas.Item)
async def upload(file: UploadFile, labels: str | None = None, db: Session = Depends(get_db)):
    """
    Upload an image file to the database. This is the main upload route. All incoming pictures will be processed here

    :param db: the database session
    :param file: the image to upload
    :param labels: the tags to add to the image as a list
    :return: a message if the file was saved or an error cure
    """
    def save() -> str:
        # process the incoming file and save it according to the structure
        # replace underscores and spaces with dashes
        file.filename = file.filename.replace(" ", "-").replace("_", "-")
        # save the incoming file
        file.filename = FolderTools().getNextFilePosition() + file.filename
        with open(file.filename, "wb") as f:
            f.write(file.file.read())
        return file.filename

    # handle request if labels are used as parameter
    if labels is not None:
        try:
            string_list = ast.literal_eval(labels)

            if isinstance(string_list, list) and all(isinstance(item, str) for item in string_list):
                return crud.create_item(db, schemas.ItemCreate(path=save(), labels=string_list, imageMetadata={}))
            else:
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
        return crud.create_item(db, schemas.ItemCreate(path=save(), labels=[], imageMetadata={}))
