"""
simple label tools for the api. This file contains some usefully functions for label management. You can use the
functions to detect duplications or find duplicated labels. This class is mostly used for cleaning up the database
and filesystem
"""
from __future__ import annotations
import ast


class LabelTools:
    """
    simple class to handle labels inside the database. This can be used to handle new labels
    """
    labelList: list[str]
    __valid: bool

    def __init__(self, labels: str | list[str]):
        """
        Create a new LabelTools object. You can pass a string or a list of strings to the constructor. If you pass
        a string, the labels will automatically be parsed into list of strings. Duplications will be removed
        automatically.

        :param labelString: the labels as a string. Example: "['label1', 'label2', 'label3']"
        :param labelList: a list full of labels as strings
        """
        try:
            if isinstance(labels, str):
                # parse the string to label list
                self.labelList = self.__parseLabels(labels)
            elif isinstance(labels, list):
                for label in labels:
                    if not isinstance(label, str):
                        raise ValueError("labels must be a list of strings")
            self.__valid = True
        except ValueError:
            self.__valid = False

    def findDuplicates(self) -> None:
        """
        simple function to find duplicates inside the labelList. This function will automatically remove duplicates
        inside the labelList of the class instance.

        :return: nothing to return
        """
        # TODO: implement
        pass

    @staticmethod
    def __parseLabels(labelString: str) -> list[str]:
        """
        parse the labelString into a list of strings. This function will only use the labels inside the labelString,
        which can be extracted. If there are any items or values with another type then a string, they will be ignored.

        :param labelString: the labelString to parse. This should start with "[" and end with "]", otherwise there is
            nothing to parse.
        :return: the labels inside a list as strings
        """
        string_list = ast.literal_eval(labelString)

        if isinstance(string_list, list) and all(isinstance(item, str) for item in string_list):
            return string_list
        raise ValueError

    def isValid(self) -> bool:
        """
        check if a labelString is valid. This can be used to determine if a incoming string is a valid labelString or
        not.

        :return: boolean value if the labelString is valid or not
        """
        return self.__valid
