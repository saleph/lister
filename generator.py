import json


class Attribute(object):
    """
    Stores an indexes of an attribute used in lists of readers.
    """
    person_id = 0
    name = 1
    lection = 2
    psalm = 3
    believers_pray = 4


class List(object):
    """
    List of available people and their lection preferences.
    Each person has 3 fields describing state of relation towards a lection:
    e.g. value of 'psalm' == -1 mean the person doesn't want to be appointed
    to this function. value >= 0 describing readiness to be appointed
    """
    def __init__(self):
        self.list = []
        self.load_list()

    def load_list(self):
        """Loads data from 'list.json' and place it into 'self.list'."""
        with open("list.json") as file:
            self.list = json.loads(file.read())

    def add_new_person(self, name, lection, psalm, believers_pray):
        """Add new person at the end of self.list and update 'list.json'."""
        name_validity = isinstance(name, str)
        lection_validity = isinstance(lection, int)
        psalm_validity = isinstance(psalm, int)
        believers_pray_validity = isinstance(believers_pray, int)

        if name_validity and lection_validity and psalm_validity and believers_pray_validity:
            # get last id from list (if exist) and increment
            if len(self.list) > 0:
                new_id = self.list[-1][0] + 1
            else:
                new_id = 0

            self.list.append([new_id, name, lection, psalm, believers_pray])
            self.file_list_update()
            return True
        else:
            return False
