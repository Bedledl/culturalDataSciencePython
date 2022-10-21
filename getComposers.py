from typing import Tuple, Union
import re

import wikipediaapi
from unidecode import unidecode

'''
this string may match:
um 1697 – um 1759
1713?–1781
* um 1500; † um 1561
'''
DATUM_BIRTH_REGEX = "\s*(um|~|vor|nach|≈)?\s*(?P<birth>\d{4,4})(\?)?"
DATUM_DEATH_REGEX = "\s*(um|~|vor|nach|≈)?\s*(?P<death>\d{4,4})(\?)?"

DATES_REGEXES = [
    re.compile(f"{DATUM_BIRTH_REGEX}((\s*-\s*)|(\s*bis\s*)|\s*–\s*){DATUM_DEATH_REGEX}"),
    re.compile(f"{DATUM_BIRTH_REGEX}; †\s*{DATUM_DEATH_REGEX}"),
    re.compile(f"\*\s*{DATUM_BIRTH_REGEX}"),
    re.compile(f"†\s*{DATUM_DEATH_REGEX}"),
    re.compile(DATUM_BIRTH_REGEX)
]



class Composer:
    def __init__(self, first_name: str, last_name: str, geburtsjahr, todesjahr, original_string=""):
        if not last_name:
            raise ValueError(f"No last name is given {original_string}.")
        self.first_name = first_name
        self.last_name = last_name
        self.geburtsjahr = geburtsjahr
        self.todesjahr = todesjahr
        self.original_str = original_string

    def __str__(self):
        return f"Last_Name{self.last_name} FirstName: {self.first_name} {self.geburtsjahr} {self.todesjahr}"


def get_first_second_name(composer_str: str, prefix_second_name) -> Tuple[str, str]:
    '''

    :param composer_str: should only contain the name part
    :param prefix_second_name: raw prefix for thhe current section
    :return: Tuple of other and second name
    '''
    first_names, second_names = [], []
    second_name_current = True

    str_split = composer_str.split()
    str_split.reverse()

    for split_str in str_split:
        if second_name_current:
            if split_str.startswith(prefix_second_name):
                second_names.append(split_str)
                second_name_current = False

        else:
            first_names.append(split_str)

    if not second_names:
        print(f"No second name found in {composer_str} with prefix {prefix_second_name}")
        ValueError(f"No second name found in {composer_str} with prefix {prefix_second_name}")

    return " ".join(first_names), " ".join(second_names)


def get_geburts_todes_jahr(composer_str: str) -> Tuple[Union[int, None], Union[int, None]]:
    '''

    :param composer_str: should ony contain the date part without brackets
    :return: Tuple of birth and death year
    '''
    birth, death = None, None
    for date_regex in DATES_REGEXES:
        m = date_regex.search(composer_str)
        if not m:
            continue

        try:
            birth = m.group("birth")
        except IndexError:
            pass
        if birth:
            birth = int(birth)
        try:
            death = m.group("death")
        except IndexError:
            pass
        if death:
            death = int(death)

        return birth, death

    if not (birth or death):
        raise ValueError(f"Composer String does not contain a Birth und Deathyear {composer_str}")

    return birth, death


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
                composer_string = unidecode(composer_string)
                try:
                    first_name, second_name = get_first_second_name(composer_string, section_prefix)
                    geburts_jahr, todesjahr = get_geburts_todes_jahr(composer_string)
                    composers.append(Composer(first_name, second_name, geburts_jahr, todesjahr))
                except ValueError as excp:
                    print(excp)

    return composers


def get_composer_from_country():
    pass
