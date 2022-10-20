from typing import Tuple, Union

import wikipediaapi


class Composer:
    def __init__(self, first_name: str, last_name: str, geburtsjahr, todesjahr):
        if not last_name:
            raise ValueError("No last name is given.")
        self.first_name = first_name
        self.last_name = last_name
        self.geburtsjahr = geburtsjahr
        self.todesjahr = todesjahr

    def __str__(self):
        return f"Last_Name{self.last_name} FirstName: {self.first_name} {self.geburtsjahr} {self.todesjahr}"


def get_first_second_name(composer_str: str, prefix_second_name) -> Tuple[str, str]:
    first_names = []
    second_names = []
    first_name_current = True
    str_split = composer_str.split()
    for split_str in str_split:
        if split_str.startswith(prefix_second_name):
            first_name_current = False

        elif split_str.startswith("("):
            return " ".join(first_names), " ".join(second_names)

        if first_name_current:
            first_names.append(split_str)
        else:
            second_names.append(split_str)

    return " ".join(first_names), " ".join(second_names)


def get_geburts_todes_jahr(composer_str: str) -> Tuple[int, Union[int, None]]:
    def extract_digits(string: str, count_digits: int):
        digits_str = "".join([letter for letter in string if letter.isdigit()])
        if len(digits_str) != count_digits:
            raise ValueError(f"Composer String does not contain a Birth und Deathjahr {composer_str}({digits_str})")

        return digits_str

    start = composer_str.index("(")
    end = composer_str.index(")")
    first_digit = composer_str[start + 1]
    if first_digit == "*":
        birth_year = extract_digits(composer_str[start+3:], 4)
        return int(birth_year), None
    elif first_digit == "†":
        death_year = extract_digits(composer_str[start+3:], 4)
        return None, int(death_year)

    jahre_str = composer_str[start+1: end]
    jahre_str = extract_digits(jahre_str, 8)

    if len(jahre_str) != 8:
        raise ValueError(f"Composer String does not contain a Birth und Deathjahr {composer_str}")

    return int(jahre_str[:4]), int(jahre_str[4:])


def get_all_composers():
    wiki = wikipediaapi.Wikipedia('de')
    composers = []

    for letter in range(ord("A"), ord("Z") + 1):
        letter = chr(letter)
        page = wiki.page(f"Liste der Komponisten/{letter}")
        sections = page.sections
        for sec in sections:
            composer_strings = sec.text.split("\n")
            section_prefix = sec.title
            for composer_string in composer_strings:
                try:
                    first_name, second_name = get_first_second_name(composer_string, section_prefix)
                    geburts_jahr, todesjahr = get_geburts_todes_jahr(composer_string)
                    composers.append(Composer(first_name, second_name, geburts_jahr, todesjahr))
                except ValueError as excp:
                    print(excp)

    return composers


def get_composer_from_country():
    pass
