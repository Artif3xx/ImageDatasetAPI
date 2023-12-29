# file to import a csv file into the database
# this function should only be used after an update of the database structure
# normally this function will only be called from the system itself

import pandas as pd
import pickle

from fastapi import Depends
from sqlalchemy.orm import Session
from api.src.database import crud, schemas
from api.src.database.database import get_db

from api.src.tools.HashTools import HashTools


def migrate_csv(csv_path: str, db: Session = Depends(get_db)):
    """
    migrate a csv file into the database

    :param csv_path: the path to the csv file
    :param db: the database session
    :return: None
    """
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)

    for index, row in df.iterrows():
        print(index, type(row['id']), type(row["path"]), type(row['imageMetadata']), type(row['labels']))

        # create the item
        path = "/Users/georg/PycharmProjects/DatasetAPI/" + str(row["path"]).replace("./", "")
        image_hash = HashTools(path).get_hash()
        # labels = str(row["labels"]).removeprefix("b'").removesuffix("'").replace('\\\\', '\\').encode("utf-8")
        # labels.replace("\\\\", "\\")
        hex_string = str(row["labels"]).split("'")[1].encode('utf-8')
        print(hex_string)
        unpickled_object = pickle.loads(hex_string)
        print(unpickled_object)
        item = schemas.ItemCreate(
            path=row["path"],
            labels=unpickled_object,
            imageMetadata=row["imageMetadata"],
            sha256_digest=image_hash
        )
        print(item)


if __name__ == "__main__":
    migrate_csv("/Users/georg/PycharmProjects/DatasetAPI/data/backup.csv")
