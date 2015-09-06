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
        with open("list.json", 'r') as file:
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
            self.json_file_update()
            return True
        else:
            return False

    def delete_person(self, name):
        """
        Removes person from the list.
        Handling situation when exist more than one the same names is unnecessary -
        it doesn't have an influence for second person.
        """
        for i in range(len(self.list)):
            if name in self.list[i]:
                del self.list[i]
                self.json_file_update()
                return True

        return False

    def json_file_update(self):
        """Override file list.json with new self.list."""
        with open("list.json", 'w') as file:
            file.write(json.dumps(self.list))

        return True
