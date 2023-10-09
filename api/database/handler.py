from __future__ import annotations

from api.database import database as db


def insert(path: str, metadata: str, labels: str) -> dict:
    """
    Insert a new image entry into the database

    :param path: the path to the image
    :param metadata: the metadata of the image as dictionary converted into a string
    :param labels: the labels of the image as list converted into a string
    :return: a message if the image was inserted or an error cure
    """
    try:
        labels = labels.replace("\"", "'")
        sql = "INSERT INTO Images (path, metadata, labels) VALUES (?, ?, ?);"
        db.execute_sql_query(sql, data=(path, metadata, labels))
        return {"msg": "inserted Balance successfully"}
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def getImageByID(imageID: int):
    """
    Get an image database entry  by its id

    :param imageID: the id of the image
    :return: the information of the image from the database
    """
    try:
        sql = "SELECT * FROM Images WHERE id = " + str(imageID) + ";"
        item = db.execute_sql_query(sql)
        return item[0]
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def getImageByPath(path: str):
    """
    Get an image database entry by its path

    :param path: the path of the image
    :return: the information of the image from the database
    """
    try:
        sql = "SELECT * FROM Images WHERE path = '" + path + "';"
        item = db.execute_sql_query(sql)
        return item[0]
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def getImagesWithLabel(label: str):
    """
    Get all database entries with a specific label in the labels list

    :param label: the label to search for. This must be a single label and not a list of labels
    :return: the ids of the images with the label
    """
    try:
        sql_query = f"SELECT id FROM Images WHERE labels LIKE '%{label}%'"
        items = db.execute_sql_query(sql_query)
        return items
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImageByID(imageID: int, path: str, metadata: str, labels: str) -> dict:
    """
    update an image database entry by its id

    :param imageID: the id of the image to update
    :param path: the new path of the image as string
    :param metadata: the new metadata of the image as dictionary converted into a string
    :param labels: the new labels of the image as list converted into a string
    :return: a message if the image was updated or an error cure
    """
    try:
        labels = labels.replace("\"", "'")
        sql = "UPDATE Images SET path = ?, metadata = ?, labels = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(path, metadata, labels, imageID))
        return {"msg": "updated Image entry successfully"}
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImagePathByID(imageID: int, newPath: str) -> dict:
    """
    update the path of an image database entry by its id

    :param imageID: the id of the image to update
    :param newPath: the new path of the image as string
    :return: a message if the image was updated or an error cure
    """
    try:
        sql = "UPDATE Images SET path = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(newPath, imageID))
        return {"msg": "updated Image path successfully"}
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImageMetadataByID(imageID: int, newMetadata: str) -> dict:
    """
    update the metadata of an image database entry by its id

    :param imageID: the id of the image to update
    :param newMetadata: the new metadata of the image as dictionary converted into a string
    :return: a message if the image was updated or an error cure
    """
    try:
        sql = "UPDATE Images SET metadata = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(newMetadata, imageID))
        return {"msg": "updated Image metadata successfully"}
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImageLabelsByID(imageID: int, newLabels: str) -> dict:
    """
    update the labels of an image database entry by its id

    :param imageID: the id of the image to update
    :param newLabels: the new labels of the image as list converted into a string
    :return: a message if the image was updated or an error cure
    """
    try:
        newLabels = newLabels.replace("\"", "'")
        sql = "UPDATE Images SET labels = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(newLabels, imageID))
        return {"msg": "updated Image labels successfully"}
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def deleteImageByID(imageID: int) -> dict:
    """
    delete an image database entry by its id

    :param imageID: the id of the image to delete
    :return: a message if the image was deleted or an error cure
    """
    try:
        sql = "DELETE FROM Images WHERE id = ?;"
        db.execute_sql_query(sql, data=(imageID,))
        return {"msg": "deleted Image successfully"}
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def getTableLength() -> int | dict:
    """
    Get the length of the table. This means the number of images in the database or the last id. Be aware that if you
    delete an id from the database the length will change but the id will not be reused.

    :return: the length of the table as integer
    """
    try:
        sql = "SELECT COUNT(*) FROM Images"
        item = db.execute_sql_query(sql)
        return int(item[0]["COUNT(*)"])
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}
