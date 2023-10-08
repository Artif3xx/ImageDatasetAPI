from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import FileResponse
import os
import random
import ast

from api.database import handler as db

router = APIRouter()


@router.get("/random")
async def getRandom(labels: str | None = None):
    if labels is None:
        maxID = db.getTableLength()
        useID = random.randint(1, maxID)
    else:
        if labels.startswith("[") and labels.endswith("]") or "\n" in labels:
            ids = {}
            try:
                if "\n" in labels:
                    labels: [str] = labels.split("\n")
                else:
                    labels = ast.literal_eval(labels)
            except ValueError:
                return {"error": "invalid label", "type": "ValueError"}
            finally:
                for item in labels:
                    if not isinstance(item, str):
                        return {"error": "invalid label", "type": "ValueError"}
                    else:
                        ids[item] = [i["id"] for i in db.getImagesWithLabel(item)]

                for item in ids:
                    ids[item] = set(ids[item])

                duplicates = list(set.intersection(*ids.values()))
                if len(duplicates) == 0:
                    return {"error": "no images found with these labels", "type": "ValueError"}
                useID = duplicates[random.randint(0, len(duplicates) - 1)]
        else:
            items = db.getImagesWithLabel(labels)
            ids = []
            for item in items:
                ids.append(item["id"])

            if len(ids) == 0:
                return {"error": "no images found with these labels", "type": "ValueError"}
            useID = ids[random.randint(0, len(ids) - 1)]
        print(labels)

    image_path = db.getImageByID(useID)["path"]

    if os.path.exists(image_path):
        return FileResponse(image_path, headers={"Content-Type": "image/jpeg"})
    else:
        return {"error": "Bild nicht gefunden"}


