import json

from sqlalchemy import create_engine, inspect, text, PickleType, VARCHAR
from sqlalchemy.orm import sessionmaker

import os
import pandas as pd
import pickle
import chardet

from api.src.database import models
from api.src.database.database import engine
from api.src.tools.HashTools import HashTools
from api.src.database import models
from api.src.database.database import Base

from sqlalchemy import Column, Integer, String, JSON, PickleType
from api.src.database.update.csv_migration import migrate_csv

from fastapi import Depends
from sqlalchemy.orm import Session
from api.src.database import crud, schemas
from api.src.database.database import get_db

from api.src.tools.HashTools import HashTools


class DatabaseUpdater:
    def __init__(self, database_path: str):
        # SQLite-Datenbankdatei
        SQLALCHEMY_DATABASE_URL = "sqlite:///" + database_path
        print(f"Using database: {SQLALCHEMY_DATABASE_URL}")

        # SQLAlchemy-Engine erstellen
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

        # SQLAlchemy-Inspector erstellen
        self.inspector = inspect(engine)

        # Verbindung zur Datenbank herstellen
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.db = SessionLocal()

    def print_table_info(self, table_name):
        print(f"Table: {table_name}")

        # Spalteninformationen abrufen
        columns = self.inspector.get_columns(table_name)
        for column in columns:
            print(f"  Column: {column['name']} - Type: {column['type']}")

    def get_table_data(self, table_name):
        print(f"Reading data from table {table_name}")

        # Beispielabfrage, um Daten aus der Spalte zu lesen
        query_result = self.db.execute(text(f"SELECT * FROM {table_name}")).fetchall()

        res_arr = []
        # Ausgabe der Ergebnisse
        for result in query_result:
            res_arr.append(result)
        return query_result

    def close(self):
        self.db.close()


def rename_to_backup_database(prod_path: str):
    # Datenbankdatei kopieren
    root_path = os.path.dirname(prod_path)
    if not os.path.exists(root_path + '/Database_backup.db'):
        os.system(f"mv {prod_path} {root_path + '/Database_backup.db'}")
        return root_path + '/Database_backup.db'

    print("Backup database already exists")
    return root_path + '/Database_backup.db'


def create_database():
    models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    prod_database_path: str = "/Users/georg/PycharmProjects/DatasetAPI/data/Database.db"
    # backup_database_path = rename_to_backup_database(prod_database_path)
    updater = DatabaseUpdater(prod_database_path)

    # Beispiel: Tabelle "your_table"
    table_name = "Images"

    # Informationen über die Tabelle ausgeben
    updater.print_table_info(table_name)

    # Beispiel: Daten aus der Spalte "existing_column" lesen
    base_path = "/Users/georg/PycharmProjects/DatasetAPI/"
    data = updater.get_table_data(table_name)
    all_items = []
    for item in data:
        item_data = {
            'item_id': item[0],
            'item_path': item[1],
            'item_imageMetadata': json.loads(item[2]),
            'item_labels': pickle.loads(item[3], encoding='Latin-1'),
            'image_hash': HashTools(base_path + item[1].removesuffix('./')).get_hash()
        }
        all_items.append(item_data)
        # print(item_id, item_path, item_labels, item_imageMetadata)

        new_item = schemas.ItemCreate(
            path=item_data['item_path'],
            labels=item_data['item_labels'],
            imageMetadata=item_data['item_imageMetadata'],
            sha256_digest=item_data['image_hash']
        )

    df = pd.DataFrame(all_items)
    print(df)

        # print(pickle.loads(item, encoding='Latin-1'))
    # df = pd.DataFrame(updater.get_table_data(table_name))
    df.to_csv(os.path.dirname(prod_database_path) + "/backup.csv", index=False)

    # Schließe die Datenbankverbindung
    updater.close()
