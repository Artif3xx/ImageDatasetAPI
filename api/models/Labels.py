
class Labels:
    labels: [str] = []
    imageID: int = None

    def __init__(self, labels: [str] = None, imageID: int = None):
        if labels is not None:
            self.labels = labels
        if imageID is not None:
            self.imageID = imageID

    def asJson(self):
        data = {
            "labels": self.labels
        }
        if self.imageID is not None:
            data["imageID"] = self.imageID

        return data
