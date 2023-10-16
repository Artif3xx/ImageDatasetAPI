import os
from logging import getLogger

Logger = getLogger(__name__)


class FolderTools:
    """
    This class is used to handle the folder structure of the database. It will create new folders if needed and return
    """
    dataFolder: str = ""

    def __init__(self, dataFolder: str = "./data/"):
        """
        Create a new FolderTools object

        :param dataFolder: the datafolder of the project. This folder will be used to store the images. The default
        value is "data/"
        """
        self.dataFolder = dataFolder if dataFolder.endswith("/") else dataFolder + "/"

    def createFolder(self, path: str) -> None:
        """
        Create a new folder in the data folder

        :param path: the path of the new folder
        :return: nothing to return
        """
        if not os.path.exists(self.dataFolder + path):
            os.makedirs(self.dataFolder + path)

    def getNextFilePosition(self) -> str:
        """
        Get the next file position in the database. This function will return the path to the next file position in the
        database. If the database is full, it will create a new folder and return the path to the first file position in
        the new folder.

        :return: a string containing the path to the next file position
        """
        dirs = os.listdir(self.dataFolder)
        folders = []
        for item in dirs:
            if not os.path.isfile(self.dataFolder + item):
                folders.append(item)

        if len(folders) == 0:
            self.createFolder("1-100")
            Logger.info("Created new folder: 1-100")
            return self.dataFolder + "1-100/1-"

        folders.sort(key=lambda x: int(x.split('-')[-1]), reverse=False)

        files = os.listdir(self.dataFolder + folders[-1])
        amount = len(files)
        if amount < 100:
            return self.dataFolder + folders[-1] + "/" + str(int(folders[-1].split('-')[0]) + amount) + "-"
        else:
            newFolder = str(int(folders[-1].split('-')[0]) + 100) + "-" + str(int(folders[-1].split('-')[1]) + 100)
            self.createFolder(newFolder)
            Logger.info(f"Created new folder: {newFolder}")
            return self.dataFolder + newFolder + "/" + str(int(folders[-1].split('-')[0]) + 100) + "-"

    @staticmethod
    def deleteFile(filepath: str) -> bool:
        """
        Delete a file from the filesystem

        :param filepath: the path to the file to delete
        :return: True if the file was deleted, False if not
        """
        try:
            os.remove(filepath)
            Logger.info(f"Deleted file: {filepath}")
            return True
        except Exception as e:
            Logger.error(f"error: {str(e)}")
            return False
