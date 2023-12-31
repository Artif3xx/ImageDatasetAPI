"""
this file contains the /search endpoints for the api
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Depends

from api.src.database import crud
from api.src.database.database import get_db
from api.src.tools.LabelTools import LabelTools


router = APIRouter()


@router.get("/search", tags=["Search Routes"])
async def get_image_ids_with_labels(labels: str, onlyOne: bool | None = None, onlyIDs: bool | None = None,
                                    db=Depends(get_db)):
    """
    Get all imageIDs that have the given labels. The labels must be passed as a list. Example: ["label1", "label2"] You
    need at least one label to search for. If you want to search for multiple labels, you can pass them as a list. \f

    :param onlyOne: true if the item should only contain one label
    :param onlyIDs: true if only the ids should be returned
    :param db: the session database to use
    :param labels: the labels to search for. Example: ["label1", "label2"]
    :return: the imageIDs that have the given labels
    """

    try:
        labelTools = LabelTools(labels)
        if labelTools.isValid():
            if onlyIDs:
                items = crud.get_items_by_label(db, labels=labelTools.labelList, onlyOne=onlyOne if onlyOne is not None else False)
                item_ids = [item.id for item in items]
                return item_ids
            return crud.get_items_by_label(db, labels=labelTools.labelList, onlyOne=onlyOne if onlyOne is not None else False)
        raise HTTPException(status_code=400, detail={
            "message": "labels must be a list of stings formatted as a string",
            "labels": labels,
            "example": f"[\'label1\', \'label2\']"})
    except (SyntaxError, ValueError) as e:
        raise HTTPException(status_code=400, detail={
            "message": "labels must be a list of stings formatted as a string",
            "labels": labels,
            "example": f"[\'label1\', \'label2\']",
            "error": str(e)})
