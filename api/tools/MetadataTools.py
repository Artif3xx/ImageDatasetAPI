from PIL import Image, ExifTags
import json

# this tags will be ignored when loading the metadata
ignoreTags = ['MakerNote', 'Location', 'Latitude', 'Altitude', 'AppleID', 'GPSInfo']


class MetadataTools:
    """
    This class provides methods to load and print the metadata of an image file.
    """

    ImagePath: str = None
    Model: str = None
    ExifImageWidth: int = None
    ExifImageHeight: int = None
    ShutterSpeedValue: float = None
    ApertureValue: float = None
    BrightnessValue: float = None
    ExposureBiasValue: float = None
    ExposureTime: float = None
    SensingMethod: int = None
    ExposureProgram: int = None
    ISOSpeedRatings: int = None
    ExposureMode: int = None
    LensSpecification: tuple = None
    LensModel: str = None
    CompositeImage: int = None
    FocalLength: float = None
    WhiteBalance: int = None

    rawMetadata: dict = None

    def __init__(self, imagePath: str) -> None:
        """
        Initialize the class and load the metadata from the image file.
        :param imagePath: the path to the image file to load the metadata from
        """
        self.ImagePath = imagePath
        self.collectMetadata()

    def collectMetadata(self) -> None:
        """
        Collect the metadata from the image file and save it as attributes of this class.
        """
        itemsToCollect = ['Model', 'ExifImageWidth', 'ExifImageHeight', 'ShutterSpeedValue', 'ApertureValue',
                          'BrightnessValue', 'ExposureBiasValue', 'ExposureTime', 'SensingMethod', 'ExposureProgram',
                          'ISOSpeedRatings', 'ExposureMode', 'LensSpecification', 'LensModel', 'CompositeImage',
                          'FocalLength', 'WhiteBalance']

        self.rawMetadata = self.loadMetadata(self.ImagePath)

        # iterate over all items to collect
        for item in itemsToCollect:
            try:
                # if the item is in the metadata, save it as an attribute of this class
                if item in self.rawMetadata:
                    setattr(self, item, self.rawMetadata[item])
            except TypeError:
                # if the item cant be load from the metadata, continue to prevent an error
                continue

    def getMetadata(self) -> dict:
        """
        get the raw metadata as a dictionary. This can contain unhandled metadata that can cause errors.
        """
        return self.rawMetadata

    def getMetadataAsJson(self) -> json:
        """
        get the metadata as a json string

        :return: the metadata as a json string
        """
        return json.dumps(self.rawMetadata, skipkeys=True, default=str)

    @staticmethod
    def loadMetadata(path: str) -> dict:
        """
        Load the metadata from an image file. The metadata will be returned as a dictionary.

        :param path: the path to the image file
        :return: the metadata as a dictionary
        """
        with Image.open(path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                metadata = {}
                if exif_data is not None:
                    for tag_id, value in exif_data.items():
                        tag = ExifTags.TAGS.get(tag_id, tag_id)
                        try:
                            if str(tag) not in ignoreTags:
                                metadata[str(tag)] = value
                        except TypeError:
                            continue
                return metadata
            else:
                return {}

    @staticmethod
    def loadMetadataAsJson(path: str) -> json:
        """
        Load the metadata from an image file. The metadata will be returned as a json string.

        :param path: the path to the image file
        :return: the metadata as a json object
        """
        data = MetadataTools.loadMetadata(path)
        return json.dumps(data, skipkeys=True, default=str)

    @staticmethod
    def printMetadata(path: str) -> None:
        """
        Print the metadata of an image file to the console.

        :param path: the path to the image file
        """
        with Image.open(path) as img:
            exif_data = img._getexif()
            if exif_data is not None:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    print(f"{tag}: {value}")
