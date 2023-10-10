import json
import ast


class DatabaseEntry:
    """
    simple class to represent an image in the database
    """
    def __init__(self, path: str, metadata: str, labels: str, imageID: int = None):
        self.path = path
        self.metadata = json.loads(metadata)
        # TODO: check if the labels are a list with strings as a string
        self.labels = ast.literal_eval(labels)
        if imageID is not None:
            self.imageID = imageID

    def asJson(self):
        """
        get the image model as a json string

        :return: the image model as a json string
        """

        data = {
            "path": self.path,
            "metadata": self.metadata,
            "labels": self.labels
        }
        if hasattr(self, 'imageID'):
            data["imageID"] = self.imageID

        return data

    def getLabels(self):
        """
        get the labels of the image database Entry in a dictionary

        :return: the labels as a json string
        """
        # create a datastructure that can be converted to json
        data = {
            "labels": self.labels
        }
        if hasattr(self, 'imageID'):
            data["imageID"] = self.imageID

        return data
