#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json


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
    def __init__(self, name, lection=False, psalm=False, believers_pray=False, speech_number=0):
        if isinstance(name, str):
            self.name = name
        else:
            raise ValueError("name has to be a string")

        if isinstance(lection, bool) and isinstance(psalm, bool) and isinstance(believers_pray, bool):
            self.lection = lection
            self.psalm = psalm
            self.believers_pray = believers_pray
        else:
            raise ValueError("lection/psalm/believers_pray field has to be a boolean")

        # if every boolean field is False, raise ValueError
        if not (lection or psalm or believers_pray):
            raise ValueError("at least one boolean field has to be True")

        if isinstance(speech_number, int):
            self.speech_number = speech_number
        else:
            raise ValueError("speech_number has to be an integer")

    def as_list(self):
        return [self.name, self.lection, self.psalm, self.believers_pray, self.speech_number]


class ListOfReaders:
    def __init__(self):
        try:
            with open('list_of_readers.json') as json_file:
                for reader_data in json_file.readlines():
                    self.list_of_readers.append(Reader(reader_data))
        except (FileNotFoundError, IOError):
            self.list_of_readers = []

    def add_reader(self, name, **kwargs):
        # check if reader with name 'name' exist - if True raise ValueError
        for reader in self.list_of_readers:
            if reader.name == name:
                raise ValueError("%s already exist" % name)

        new_reader = Reader(name=name, **kwargs)
        self.list_of_readers.append(new_reader)
        with open('list_of_readers.json', 'a') as json_file:
            json_file.writelines(new_reader.as_list())

    def delete_reader(self, name) -> bool:
        for idx, reader in enumerate(self.list_of_readers):
            if reader.name == name:
                self.list_of_readers.pop(idx)
                self.dump_list_of_readers_to_json()
                return True
        return False

    def dump_list_of_readers_to_json(self):
        try:
            with open('list_of_readers.json', 'w') as json_file:
                for reader in self.list_of_readers:
                    json_file.writelines(json.dumps(reader.as_list()))
        except IOError:
            print("json dumping error or json file privileges error")


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
