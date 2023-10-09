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
        data = {
            "labels": self.labels
        }
        if hasattr(self, 'imageID'):
            data["imageID"] = self.imageID

        return data
