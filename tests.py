import generator


def func():
    lst = generator.List()
    lst.add_new_person("Osoba Pierwsza", True, False, False)
    lst.add_new_person("Osoba Druga", True, False, False)
    lst.add_new_person("Osoba Trzecia", False, True, False)
    lst.add_new_person("Osoba czwarta", False, False, True)
    lst.add_new_person("Osoba Piąta", True, True, False)
    lst.add_new_person("Osoba Szósta", True, False, True)

    d_a_h = [
        ["21.02.2011", True, ["9.00", "11.00", "12.00"]],
        ["23.02.2011", True, ["9.00", "11.00", "12.00"]],
        ["25.02.2011", True, ["9.00", "11.00", "12.00"]],
        ["28.02.2011", False, ["9.00", "11.00"]],
        ["40.02.2011", True, ["9.00", "11.00", "12.00", "16.00"]]
    ]
    lst.create_html_readers_list(d_a_h)


if __name__ == "__main__":
    func()
