"""
this file contains the /info endpoints for the api
"""
from __future__ import annotations
import json

from fastapi import APIRouter


router = APIRouter()


@router.get("/info")
async def get_api_info():
    """
    Get information about the image server and the api

    :return: the info as a json string
    """

    info = json.load(open("package.json"))
    return {"info": info}
