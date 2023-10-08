from fastapi import APIRouter
import ast

from api.database import handler as db
from api.models import Labels as cardModel

router = APIRouter()


@router.get("/labels")
async def getLabelsByID(imageID: int):
    imageData = db.getImageByID(imageID)
    model = cardModel.Labels(labels=imageData["labels"], imageID=imageData["id"])
    return model


@router.post("/updateLabels")
async def updateLabelsByID(imageID: int, labels: str):
    labels = labels.replace("\"", "'")
    return db.updateImageLabelsByID(imageID, labels)


@router.get("/imageIDsWithLabel")
async def getImageIDsWithLabel(label: str):
    if label.startswith("[") and label.endswith("]"):
        ids = {}
        try:
            label = ast.literal_eval(label)
        except ValueError:
            return {"error": "invalid label", "type": "ValueError"}
        finally:
            for item in label:
                if not isinstance(item, str):
                    return {"error": "invalid label", "type": "ValueError"}
                else:
                    ids[item] = [i["id"] for i in db.getImagesWithLabel(item)]

            for item in ids:
                ids[item] = set(ids[item])

            duplicates = set.intersection(*ids.values())

            return duplicates

    # print(label)

    items = db.getImagesWithLabel(label)
    ids = []
    for item in items:
        ids.append(item["id"])

    return {"imageIDs": ids}
