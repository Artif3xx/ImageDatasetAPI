from __future__ import annotations

from fastapi import APIRouter, File, UploadFile
from api.tools.metadata import MetadataTools
from api.tools.folders import FolderTools
from api.database import handler as db

router = APIRouter()


@router.post('/upload')
async def upload_file(file: UploadFile, labels: str | None = None):
    """
    Upload an image file to the database. This is the main upload route. All incoming pictures will be processed here

    :param file: the image to upload
    :param labels: the tags to add to the image as a list
    :return: a message if the file was saved or an error cure
    """

    labels: [str] = labels.split("\n") if labels is not None else []
    # print(labels)

    # process the incoming file and save it according to the structure
    await handleIncomingImage(file=file, labels=labels)

    # Hier kannst du eine Antwort zurückgeben, um den Client zu informieren, dass das Bild empfangen wurde.
    return {"message": "Bild erfolgreich empfangen und gespeichert"}


async def handleIncomingImage(file: UploadFile, labels: list) -> None:
    """
    Handle the incoming image file. This function will save the image to the database and process it

    :param file: the image to handle
    :param labels: the tags to add to the image
    :return: None
    """
    # replace underscores and spaces with dashes
    file.filename = file.filename.replace(" ", "-").replace("_", "-")
    # save the incoming file
    file.filename = FolderTools().getNextFilePosition() + file.filename
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    metadata = MetadataTools(file.filename)
    # if labels are empty, set them to the model name
    if not labels:
        labels = [metadata.Model] if metadata.Model is not None else []

    # add the model to the labels if it is not already in the labels
    if metadata.Model not in labels and metadata.Model is not None:
        labels.append(metadata.Model)

    # insert the new image into the database
    db.insert(file.filename, f"{metadata.getMetadataAsJson()}", f"{labels}")
