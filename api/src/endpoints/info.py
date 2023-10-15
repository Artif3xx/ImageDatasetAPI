from __future__ import annotations

from fastapi import APIRouter
import json


router = APIRouter()


@router.get("/info")
async def getImageInfoByID():
    """
    Get information about the image server and the api

    :return: the info as a json string
    """

    info = json.load(open("package.json"))
    return {"info": info}
