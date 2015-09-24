import generator


def func():
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
        ("2011.7.4", ("9:00", "11:00", "12:00"), False),
        ("2011.8.12", ("9:00", "11:00")),
        ("2011.12.21", ("9:00", "11:00", "12:00", "16:00"))
    )
    generator.HtmlReadersTable(d_a_h)


if __name__ == "__main__":
    func()
