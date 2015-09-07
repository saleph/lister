import json


class Attribute(object):
    """Stores an indexes of an attribute used in lists of readers."""
    person_id = 0
    name = 1
    lection = 2
    psalm = 3
    believers_pray = 4
    speech_number = 5


class List(object):
    """
    List of available people and their lection preferences.
    Each person has 3 fields describing state of relation towards a lection and speech_number
    used to sorting before new reading list generation
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
        lection_validity = isinstance(lection, bool)
        psalm_validity = isinstance(psalm, bool)
        believers_pray_validity = isinstance(believers_pray, bool)

        if name_validity and lection_validity and psalm_validity and believers_pray_validity:
            # get last id from list (if exist) and increment
            if len(self.list) > 0:
                new_id = self.list[-1][0] + 1
            else:
                new_id = 0

            self.list.append([new_id, name, lection, psalm, believers_pray, 0])
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

    def sort_by_speeches(self):
        """Sorts self.list by number of speeches."""
        self.list.sort(key=lambda person: person[Attribute.speech_number])

    def create_html_readers_list(self, days_and_hours):
        """
        Creates html file with list of readers
        :param days_and_hours: structure [["date1", ["hour1", "hour2"]], (...), ["date_n", ["hour1", (...), "hour_n"]]
        :return: True if successful, False if invalid input.
        """
        self.sort_by_speeches()

        if not self.check_dates_table(days_and_hours):
            return False

        html_file = """<!DOCTYPE html>
                    <html>
                    <head>
                    <style>
                    table, th, td {
                        border: 1px solid black;
                        border-collapse: collapse;
                    }
                    th, td {
                        padding: 5px;
                        text-align: center;
                    }
                    </style>
                    </head>
                    <body>
                    <h1>Lista czytających: %s - %s""" % (days_and_hours[0][0],
                                                         days_and_hours[-1][0])  # first and last date used in list
