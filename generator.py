import json


class Attribute(object):
    """
    Stores an indexes of an attribute used in lists of readers.
    """
    id = 0
    name = 1
    lection = 2
    psalm = 3
    believers_pray = 4


class List(object):
    """
    List of available people and their lection preferences.
    Attributes of each line in 'self.list' are the same as in 'Attribute' class.

    """
    def __init__(self):
        self.list = None
        self.load_list()

    def load_list(self):
        """Loads data from 'list.json' and place it into 'self.list'."""
        with open("list.json") as file:
            self.list = json.loads(file.read())
