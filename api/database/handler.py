from api.database import database as db


def insert(path: str, metadata: str, labels: str):
    """
    Insert a new image into the database

    :param path: the path to the image
    :param metadata: the metadata of the image as dictionary converted into a string
    :param labels: the labels of the image as list converted into a string
    :return: a message if the image was inserted or an error cure
    """
    try:
        sql = "INSERT INTO Images (path, metadata, labels) VALUES (?, ?, ?);"
        db.execute_sql_query(sql, data=(path, metadata, labels))
        return "inserted Balance successfully"
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def getImageByID(imageID: int):
    """
    Get an image by its id

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
    Get an image by its path

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
    try:
        sql_query = f"SELECT id FROM Images WHERE labels LIKE '%{label}%'"
        items = db.execute_sql_query(sql_query)
        return items
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImageByID(imageID: int, path: str, metadata: str, labels: str):
    """
    update an image by its id

    :param imageID: the id of the image to update
    :param path: the new path of the image as string
    :param metadata: the new metadata of the image as dictionary converted into a string
    :param labels: the new labels of the image as list converted into a string
    :return: a message if the image was updated or an error cure
    """
    try:
        sql = "UPDATE Images SET path = ?, metadata = ?, labels = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(path, metadata, labels, imageID))
        return "updated Image entry successfully"
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImagePathByID(imageID: int, newPath: str):
    """
    update the path of an image by its id

    :param imageID: the id of the image to update
    :param newPath: the new path of the image as string
    :return: a message if the image was updated or an error cure
    """
    try:
        sql = "UPDATE Images SET path = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(newPath, imageID))
        return "updated Image path successfully"
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImageMetadataByID(imageID: int, newMetadata: str):
    """
    update the metadata of an image by its id

    :param imageID: the id of the image to update
    :param newMetadata: the new metadata of the image as dictionary converted into a string
    :return: a message if the image was updated or an error cure
    """
    try:
        sql = "UPDATE Images SET metadata = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(newMetadata, imageID))
        return "updated Image metadata successfully"
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def updateImageLabelsByID(imageID: int, newLabels: str):
    """
    update the labels of an image by its id

    :param imageID: the id of the image to update
    :param newLabels: the new labels of the image as list converted into a string
    :return: a message if the image was updated or an error cure
    """
    try:
        sql = "UPDATE Images SET labels = ? WHERE id = ?;"
        db.execute_sql_query(sql, data=(newLabels, imageID))
        return "updated Image labels successfully"
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def deleteImageByID(imageID: int):
    """
    delete an image by its id

    :param imageID: the id of the image to delete
    :return: a message if the image was deleted or an error cure
    """
    try:
        sql = "DELETE FROM Images WHERE id = ?;"
        db.execute_sql_query(sql, data=(imageID,))
        return "deleted Image successfully"
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}


def getTableLength():
    try:
        sql = "SELECT COUNT(*) FROM Images"
        item = db.execute_sql_query(sql)
        return int(item[0]["COUNT(*)"])
    except (ValueError, IndexError) as e:
        return {"error": str(e), "type": type(e).__name__}
