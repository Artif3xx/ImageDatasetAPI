from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from logging import getLogger
import cv2 as cv

from statistics import ImageStatistics
from repo import main
from repo.src.tools import Image as tools

router = APIRouter()
Logger = getLogger(__name__)
allowed_content_type = ["jpeg", "jpg", "png"]


@router.post('/upload/stats')
async def upload_stats(file: UploadFile):
    if file.filename.split('.')[-1] not in allowed_content_type:
        raise HTTPException(status_code=400, detail={
            "message": "The file type is not supported",
            "file": file.filename,
            "content_type": file.content_type,
            "allowed_content_type": allowed_content_type})

    file.filename = "data/" + file.filename.replace(" ", "-").replace("_", "-")

    def save(filepath):
        # save the incoming file
        with open(filepath, "wb") as f:
            f.write(file.file.read())
        Logger.info(f"file saved: {file.filename}")

    save(file.filename)

    stats = ImageStatistics.ImageStatistics(file.filename)
    image = tools.Image.resize(main.getBlade(stats.get_image()), 720)
    res = ImageStatistics.ImageStatistics.write_values_on_image(image, stats.get_statistics())
    cv.imwrite(file.filename + "_stats.png", img=res)

    return FileResponse(file.filename + "_stats.png", headers={"Content-Type": "image/jpeg"})
