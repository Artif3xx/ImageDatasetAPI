

class LabelTools:
    """
    simple class to handle labels inside the database. This can be used to handle new labels
    """
    def __init__(self, labelString: str = None, labelList: list[str] = None):
        """
        Create a new LabelTools object. You can pass a string or a list of strings to the constructor. If you pass
        a string, the labels will automatically be parsed into list of strings. Duplications will be removed
        automatically.

        :param labelString: the labels as a string. Example: "['label1', 'label2', 'label3']"
        :param labelList: a list full of labels as strings
        """
        # check if only a labelString is passed
        if labelString is not None and labelList is None:
            self.labelString = labelString

        # check if only a labelList is passed
        if labelList is not None and labelString is None:
            self.labelList = labelList

        # check if the user don´t pass any parameter to the constructor
        if labelString is None and labelList is None:
            raise ValueError("You must pass at least one parameter to the constructor")

        # check if the user pass more than one parameter to the constructor
        if labelString is not None and labelList is not None:
            raise ValueError("You can only pass one parameter to the constructor")

    def findDuplicates(self) -> None:
        """
        simple function to find duplicates inside the labelList. This function will automatically remove duplicates
        inside the labelList of the class instance.

        :return: nothing to return
        """
        # TODO: implement
        pass

    @staticmethod
    def parseLabels(labelString: str) -> list[str]:
        """
        parse the labelString into a list of strings. This function will only use the labels inside the labelString,
        which can be extracted. If there are any items or values with another type then a string, they will be ignored.

        :param labelString: the labelString to parse. This should start with "[" and end with "]", otherwise there is
            nothing to parse.
        :return: the labels inside a list as strings
        """
        # TODO: implement
        pass

    @staticmethod
    def isValid(labelString: str) -> bool:
        """
        check if a labelString is valid. This can be used to determine if a incoming string is a valid labelString or
        not.

        :param labelString: the labelString to check
        :return: boolean value if the labelString is valid or not
        """
        # TODO: implement
        pass
