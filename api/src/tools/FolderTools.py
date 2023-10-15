import os


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
            self.createFolder("0-100")
            print("[Info] --> Created new folder: 0-100")
            return self.dataFolder + "0-100/1-"

        folders.sort(key=lambda x: int(x.split('-')[-1]), reverse=True)

        for i in range(len(folders)):
            dirs = os.listdir(self.dataFolder + folders[i])
            amount = len(dirs)
            if amount < 100:
                return self.dataFolder + folders[i] + "/" + str(int(folders[i].split('-')[0]) + amount) + "-"
            else:
                newFolder = str(int(folders[i].split('-')[0]) + 100) + "-" + str(int(folders[i].split('-')[1]) + 100)
                self.createFolder(newFolder)
                print("[Info] --> Created new folder: " + newFolder)
                return self.dataFolder + newFolder + "/" + str(int(folders[i].split('-')[0]) + 100) + "-"
