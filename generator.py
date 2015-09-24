#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import datetime


class Attribute:
    """Stores index of an attribute used in list of readers and dates."""
    # List.list
    NAME = 0
    LECTION = 1
    PSALM = 2
    BELIEVERS_PRAY = 3
    SPEECH_NUMBER = 4

    # dates_and_hours
    DATE = 0
    IS_SECOND_LECTION = 1
    HOURS = 2


class Reader:
    """
    A reader class stores base info about one person.
    """
    def __init__(self, name, lection=False, psalm=False, believers_pray=False, speech_number=0):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("name has to be a string")

        if isinstance(lection, bool) and isinstance(psalm, bool) and isinstance(believers_pray, bool):
            self.lection = lection
            self.psalm = psalm
            self.believers_pray = believers_pray
        else:
            raise TypeError("lection/psalm/believers_pray field has to be a boolean")

        # if every boolean field is False, raise ValueError
        if not (lection or psalm or believers_pray):
            raise ValueError("at least one boolean field has to be True")

        if isinstance(speech_number, int):
            self.speech_number = speech_number
        else:
            raise TypeError("speech_number has to be an integer")

    def as_list(self):
        """Returns reader's data as list. Used in parsing json file."""
        return [self.name, self.lection, self.psalm, self.believers_pray, self.speech_number]


class ListOfReaders:
    """
    Stores instances of Reader's class and allows to edit a list stored in json file.
    """
    def __init__(self):
        self.JSON_FILE = 'list_of_readers.json'
        try:
            with open(self.JSON_FILE) as json_file:
                for reader_data in json_file.readlines():
                    self.list_of_readers.append(Reader(reader_data))
        except (FileNotFoundError, IOError):
            self.list_of_readers = []

    def add_reader(self, name, **kwargs):
        """Adds reader to the list_of_reader and to the json file."""
        # check if reader with name 'name' exist - if True raise ValueError
        for reader in self.list_of_readers:
            if reader.name == name:
                raise ValueError("%s already exist" % name)

        new_reader = Reader(name=name, **kwargs)
        self.list_of_readers.append(new_reader)
        with open(self.JSON_FILE, 'a') as json_file:
            json_file.writelines(new_reader.as_list())

    def delete_reader(self, name) -> bool:
        """Deletes reader from list_of_readers and from the json file."""
        for idx, reader in enumerate(self.list_of_readers):
            if reader.name == name:
                self.list_of_readers.pop(idx)
                self.dump_list_of_readers_to_json()
                return True
        return False

    def dump_list_of_readers_to_json(self):
        """Updates the json file after reader deletion."""
        try:
            with open(self.JSON_FILE, 'w') as json_file:
                for reader in self.list_of_readers:
                    json_file.writelines(json.dumps(reader.as_list()))
        except IOError:
            print("json dumping error or json file privileges error")

    def sort_by_speeches(self):
        """Sorts list_of_readers by speech number."""
        self.list_of_readers.sort(key=lambda reader: reader.speech_number)


class Mess:
    """
    Stores info about mess.
    """
    def __init__(self, r_list, hour, second_lection=True):
        if isinstance(hour, str):
            split_hour = hour.split(':')
            self.hour = datetime.time(*split_hour)
        elif isinstance(hour, datetime.time):
            self.hour = hour
        else:
            raise TypeError("hour has to be string or datetime.time")

        if isinstance(second_lection, bool):
            self.is_second_lection = second_lection
        else:
            raise TypeError("second_lection has to be a boolean")

        self.first_lection = self.get_reader(r_list, 'lection')
        if self.is_second_lection:
            self.second_lection = self.get_reader(r_list, 'lection')
        self.psalm = self.get_reader(r_list, 'psalm')
        self.believers_pray = self.get_reader(r_list, 'believers_pray')

    @staticmethod
    def get_reader(r_list, lection_type):
        r_list.sort_by_speeches()
        if lection_type == 'lection':
            for reader in r_list:
                if reader.lection:
                    return reader.name
        elif lection_type == 'psalm':
            for reader in r_list:
                if reader.psalm:
                    return reader.name
        elif lection_type == 'believers_pray':
            for reader in r_list:
                if reader.believers_pray:
                    return reader.name
        else:
            raise ValueError("lection_type doesn't fit to any case")


class Day:
    """
    Stores info about day (date and messes).
    :param date: yyyy.mm.dd
    """
    def __init__(self, r_list, date, messes):
        if isinstance(date, str):
            split_date = date.split('.')
            self.date = datetime.date(*split_date)
        elif isinstance(date, datetime.date):
            self.date = date
        else:
            raise TypeError("date has to be a string or datetime.date")

        self.messes_list = []
        if isinstance(messes, list):
            for mess in messes:
                if isinstance(mess, str):
                    self.messes_list.append(Mess(r_list, mess))
                elif isinstance(mess, list):
                    self.messes_list.append(Mess(r_list, *mess))
        else:
            raise TypeError("messes parameter has to be list")


# ----------------------------------------------------------------------------------------------------------------------
class List:
    """
    List of available people and their lection preferences. Each person has 3 fields describing state of relation
    towards a lection and speech_number used to sorting before new reading list generation.
    """

    def __init__(self) -> None:
        """Init the list with readers and generator's vars."""
        self.list_ = []
        self.html_file = ''
        self.load_list()

    def load_list(self):
        """Loads data from 'list.json' and place it into 'self.list_'."""
        try:
            with open("list.json", 'r') as file:
                self.list_ = json.loads(file.read())
        except FileNotFoundError:
            pass

    def add_new_person(self, name, lection, psalm, believers_pray) -> bool:
        """Add new person at the end of self.list_ and update 'list.json'."""
        name_validity = isinstance(name, str)
        lection_validity = isinstance(lection, bool)
        psalm_validity = isinstance(psalm, bool)
        believers_pray_validity = isinstance(believers_pray, bool)

        if name_validity and lection_validity and psalm_validity and believers_pray_validity:
            self.list_.append([name, lection, psalm, believers_pray, 0])
            self.json_file_update()
            return True
        else:
            return False

    def delete_person(self, name) -> bool:
        """
        Removes person from the list.
        Handling situation when exist more than one the same names is unnecessary - it doesn't have an influence
        for second person.
        """
        for i in range(len(self.list_)):
            if name in self.list_[i]:
                del self.list_[i]
                self.json_file_update()
                return True

        return False

    def json_file_update(self) -> bool:
        """Override file list.json with new self.list_."""
        with open("list.json", 'w') as file:
            file.write(json.dumps(self.list_))

        return True

    # html list generating methods
    def sort_by_speeches(self):
        """Sorts self.list_ by number of speeches."""
        self.list_.sort(key=lambda person: person[Attribute.SPEECH_NUMBER])

    def get_reader(self, lection_type) -> str:
        """Return name of person whose speech_number is smallest and his relation towards lection 'type' is True.
        :rtype:str
        """
        self.sort_by_speeches()
        for person in self.list_:
            if person[lection_type]:
                person[Attribute.SPEECH_NUMBER] += 1
                return person[Attribute.NAME]

    def create_html_readers_list(self, days_hours) -> bool:
        """
        Creates html file with list of readers.

        :param days_hours: structure: [["date1", if_second_lection, ["hour1", "hour2"]], (...),
        ["date_n", if_second_lection, ["hour1", (...), "hour_n"]]
        :return: True if successful, False if invalid input.
        """
        self.html_file = ('<!DOCTYPE html>\n'
                          '<html>\n'
                          '<head>\n'
                          '<meta charset=\"UTF-8\">\n'
                          '<style>\n'
                          'h1 {{\n'
                          '    text-align: center;\n'
                          '}}\n'
                          'table, th, td {{\n'
                          '    border: 1px solid black;\n'
                          '    border-collapse: collapse;\n'
                          '}}\n'
                          'th, td {{\n'
                          '    text-align: center;\n'
                          '}}\n'
                          '</style>\n'
                          '</head>\n'
                          '<body>\n'
                          '<h1>Lista czytających: {first} - {last}</h1>\n').format(first=days_hours[0][Attribute.DATE],
                                                                                   last=days_hours[-1][Attribute.DATE])

        self.html_file = ('{head}<table>\n'
                          '<tr>\n'
                          ' <th>Data</th>\n'
                          ' <th>Godzina</th>\n'
                          ' <th>I czytanie</th>\n'
                          ' <th>II czytanie</th>\n'
                          ' <th>Psalm</th>\n'
                          ' <th>Modlitwa wiernych</th>\n'
                          '</tr>\n').format(head=self.html_file)

        # main block of generator
        for date in days_hours:
            self.html_file = '{head}<tr>\n'.format(head=self.html_file)

            # span the same number of rows as date[Attribute.HOURS] has various hours
            self.html_file = '{head}<th rowspan="{no_hours}">{date}</th>\n'.format(head=self.html_file,
                                                                                   no_hours=len(date[Attribute.HOURS]),
                                                                                   date=date[Attribute.DATE])

            # first hour has to be written manually because of started <tr>
            first_lection = self.get_reader(Attribute.LECTION)

            # if second lection will be read
            if date[Attribute.IS_SECOND_LECTION]:
                second_lection = self.get_reader(Attribute.LECTION)
            else:
                second_lection = '-'

            psalm = self.get_reader(Attribute.PSALM)
            believers_pray = self.get_reader(Attribute.BELIEVERS_PRAY)

            self.html_file = ('{head}<th>{hour}</th>\n'
                              ' <td>{lct_1}</td>\n'
                              ' <td>{lct_2}</td>\n'
                              ' <td>{ps}</td>\n'
                              ' <td>{pray}</td>\n'
                              '</tr>\n').format(head=self.html_file, hour=date[Attribute.HOURS][0],
                                                lct_1=first_lection, lct_2=second_lection, ps=psalm,
                                                pray=believers_pray)

            for i in range(1, len(date[Attribute.HOURS])):
                first_lection = self.get_reader(Attribute.LECTION)

                # if second lection will be read
                if date[Attribute.IS_SECOND_LECTION]:
                    second_lection = self.get_reader(Attribute.LECTION)
                else:
                    second_lection = '-'

                psalm = self.get_reader(Attribute.PSALM)
                believers_pray = self.get_reader(Attribute.BELIEVERS_PRAY)

                self.html_file = ('{head}<tr>\n'
                                  ' <th>{hour}</th>\n'
                                  ' <td>{lct_1}</td>\n'
                                  ' <td>{lct_2}</td>\n'
                                  ' <td>{ps}</td>\n'
                                  ' <td>{pray}</td>\n'
                                  '</tr>\n').format(head=self.html_file, hour=date[Attribute.HOURS][i],
                                                    lct_1=first_lection, lct_2=second_lection, ps=psalm,
                                                    pray=believers_pray)

        self.html_file = ('{head}</table>\n'
                          '</body>\n'
                          '</html>').format(head=self.html_file)

        first_date_html_file = '{first} - {last}'.format(first=days_hours[0][Attribute.DATE][0:5],
                                                         last=days_hours[-1][Attribute.DATE][0:5])

        first_date_html_file = '{head}.html'.format(head=first_date_html_file)
        with open(first_date_html_file, 'w') as file:
            file.write(self.html_file)

        return True
