"""
this file contains the /info endpoints for the api
"""
from __future__ import annotations
import json

from fastapi import APIRouter, Depends
from api.src.database.database import get_db
from sqlalchemy.orm import Session
from api.src.database import crud

router = APIRouter()


@router.get("/info", tags=["info routes"])
async def get_api_info():
    """
    Get information about the image server and the api

    :return: the info as a json string
    """
    info = json.loads("api/package.json")
    return info


@router.get("/info/labels", tags=["info routes"])
async def get_labels(db: Session = Depends(get_db)):
    """
    Get all labels from the database

    :param db: the database session to use
    :return: a list of all labels
    """
    return crud.get_labels(db)
