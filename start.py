#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import generator


def func():
    """
    If u run the program first time - uncomment this block below.
    After first run you have to make this block commented again.
    Otherwise generator raise ValueError because of repetitive names.
    """
    '''lst = generator.ListOfReaders()
    lst.add_reader("Osoba Pierwsza", lection=True)
    lst.add_reader("Osoba Druga", lection=True)
    lst.add_reader("Osoba Trzecia", psalm=True)
    lst.add_reader("Osoba czwarta", believers_pray=True)
    lst.add_reader("Osoba Piąta", lection=True, psalm=True)
    lst.add_reader("Osoba Szósta", lection=True, believers_pray=True)'''

    d_a_h = (
        ("2011.5.2", ("9:00", "11:00", "12:00")),
        ("2011.6.3", ("9:00", "11:00", "12:00")),
        ("2011.7.4", ("9:00", "11:00", "12:00"), False), # in this day second lection won't be generated for each mess
        ("2011.8.12", ("9:00", "11:00")),
        ("2011.12.21", ("9:00", "11:00", "12:00", "16:00"))
    )
    generator.HtmlReadersTable(d_a_h)


if __name__ == "__main__":
    func()
