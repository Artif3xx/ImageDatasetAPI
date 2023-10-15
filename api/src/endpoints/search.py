from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends
import ast

from api.src.database import crud
from api.src.database.database import get_db


router = APIRouter()


@router.get("/search")
async def getImageIDsWithLabel(labels: str, db=Depends(get_db)):
    """
    Get all imageIDs that have the given labels. The labels must be passed as a list. Example: ["label1", "label2"] You
    need at least one label to search for. If you want to search for multiple labels, you can pass them as a list.

    :param db:
    :param labels: the labels to search for. Example: ["label1", "label2"]
    :return: the imageIDs that have the given labels
    """

    try:
        string_list = ast.literal_eval(labels)

        if isinstance(string_list, list) and all(isinstance(item, str) for item in string_list):
            return crud.get_items_by_label(db, labels=string_list)
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