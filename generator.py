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

    :param r_list: an instance of ListOfReaders
        (preventing the multiple reads from file in Mess.get_reader())
    :param hour: a string/datetime.time representation of mess hour
    :param is_second_lection: parameter inherited from Day class
    """

    def __init__(self, r_list, hour, is_second_lection):
        if isinstance(hour, str):
            split_hour = hour.split(':')
            self.hour = datetime.time(*split_hour)
        elif isinstance(hour, datetime.time):
            self.hour = hour
        else:
            raise TypeError("hour has to be string or datetime.time")

        if isinstance(is_second_lection, bool):
            self.is_second_lection = is_second_lection
        else:
            raise TypeError("second_lection has to be a boolean")

        self.first_lection = self.get_reader(r_list, 'lection')
        if self.is_second_lection:
            self.second_lection = self.get_reader(r_list, 'lection')
        else:
            self.second_lection = '---'
        self.psalm = self.get_reader(r_list, 'psalm')
        self.believers_pray = self.get_reader(r_list, 'believers_pray')

    @staticmethod
    def get_reader(r_list, lection_type) -> str:
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
    Stores info about day (date and messes_hours).

    :param r_list: an instance of ListOfReaders
        (preventing the multiple reads from file in Mess.get_reader())
    :param date: yyyy.mm.dd
    :param messes_hours: tuple with messes hours
    :param is_second_lection: optional parameter. Tells if the day has second lection.
    """

    def __init__(self, r_list, date, messes_hours, is_second_lection=True):
        if isinstance(r_list, ListOfReaders):
            pass
        else:
            raise TypeError("r_list parameter has to be instance of ListOfReaders")

        if isinstance(date, str):
            split_date = date.split('.')
            self.date = datetime.date(*split_date)
        elif isinstance(date, datetime.date):
            self.date = date
        else:
            raise TypeError("date has to be a string or datetime.date")

        self.mess = []
        if isinstance(messes_hours, tuple):
            for mess_hour in messes_hours:
                self.mess.append(Mess(r_list, mess_hour, is_second_lection))
        else:
            raise TypeError("messes_hours parameter has to be tuple")


class ReadersTable:
    """
    Stores a list with following Days.

    :param days_and_hours: a two dimension tuple. Syntax:
        (
            (date1, (hour1, hour2,...), is_second_lection),
            (date2, (hour1, hour2,...)),
            ("2015.05.29", ("11:00", "18:00"), False),
            ("2015.01.18", ("7:00",)) # second lection will be included
            ("2015.01.18", ("7:00", "17:00", "19:37"), True) # the same here
            ...
        )

    date: str, yyyy.mm.dd
    hour: str, hh:mm
    is_second_lection: bool, include only if the day has NOT second lection (False)
    """

    def __init__(self, days_and_hours):
        list_of_readers = ListOfReaders()
        self.day = []
        if isinstance(days_and_hours, tuple):
            for day_and_hours in days_and_hours:
                day = Day(list_of_readers, *day_and_hours)
                self.day.append(day)


class HtmlReadersTable:
    """
    Stores html file template and renders final readers' table.

    :param days_and_hours_tuple: a two dimension tuple. Syntax:
        (
            (date1, (hour1, hour2,...), is_second_lection),
            (date2, (hour1, hour2,...)),
            ("2015.05.29", ("11:00", "18:00"), False),
            ("2015.01.18", ("7:00",)) # second lection will be included
            ("2015.01.18", ("7:00", "17:00", "19:37"), True) # the same here
            ...
        )

    date: str, yyyy.mm.dd
    hour: str, hh:mm
    is_second_lection: bool, include only if the day has NOT second lection (False)
    """

    def __init__(self, days_and_hours_tuple):
        self.readers_table = ReadersTable(days_and_hours=days_and_hours_tuple)
        self.html_file = ''
        self.create_html_file()

    def create_html_file(self):
        """Stores a template of html file and renders it with the data from readers_table."""
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
                          '<h1>Lista czytających: {first} - {last}</h1>\n'
                          '<table>\n'
                          '<tr>\n'
                          ' <th>Data</th>\n'
                          ' <th>Godzina</th>\n'
                          ' <th>I czytanie</th>\n'
                          ' <th>II czytanie</th>\n'
                          ' <th>Psalm</th>\n'
                          ' <th>Modlitwa wiernych</th>\n'
                          '</tr>\n'
                          ).format(first=self.readers_table.day[0].date,
                                   last=self.readers_table.day[-1].date)

        # main generator's block
        for day in self.readers_table.day:
            self.html_file += '<tr>\n'
            self.html_file += '<th rowspan="{no_messes}">{date}</th>\n'.format(no_messes=len(day.mess),
                                                                               date=day.date)

            # first mess need to be written manually because of started <tr> near date
            mess = day.mess[0]
            self.html_file += ('<th>{hour}</th>\n'
                               ' <td>{lct_1}</td>\n'
                               ' <td>{lct_2}</td>\n'
                               ' <td>{ps}</td>\n'
                               ' <td>{pray}</td>\n'
                               '</tr>\n'
                               ).format(hour=mess.hour, lct_1=mess.first_lecition,
                                        lct_2=mess.second_lection, ps=mess.psalm,
                                        pray=mess.believers_pray)

            # for left messes of day
            for mess in day.mess[1:]:
                self.html_file += ('<th>{hour}</th>\n'
                                   ' <td>{lct_1}</td>\n'
                                   ' <td>{lct_2}</td>\n'
                                   ' <td>{ps}</td>\n'
                                   ' <td>{pray}</td>\n'
                                   '</tr>\n'
                                   ).format(hour=mess.hour, lct_1=mess.first_lecition,
                                            lct_2=mess.second_lection, ps=mess.psalm,
                                            pray=mess.believers_pray)
        self.html_file += ('</table>\n'
                           '</body>\n'
                           '</html>')

        html_file_name = '{first} - {last}.html'.format(first=self.readers_table.day[0].date,
                                                        last=self.readers_table.day[-1].date)

        with open(html_file_name, 'w') as file:
            file.write(self.html_file)
