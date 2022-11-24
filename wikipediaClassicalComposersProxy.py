import pickle
from typing import Tuple, Union, List
import re

import wikipediaapi

from Composer import Composer
from helper import unidecode_except_german_umlaute

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

COMPOSER_STRING_REGEX = "(?P<name>[^\(\)]*) ?(\([^\(\)]*\))? ?\((?P<year>[^\(\)]*)\)"
PREFIX_NAME_MATCHING_REGEX = "([LDd]')?{prefix}"


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

    regex = re.compile(PREFIX_NAME_MATCHING_REGEX.format(prefix=prefix_second_name))

    for split_str in str_split:
        if second_name_current:
            second_names.append(split_str)
            if split_str.startswith(prefix_second_name) or regex.fullmatch(split_str):
                second_name_current = False

        else:
            first_names.append(split_str)

    if not second_names:
        print(f"No second name found in {composer_str} with prefix {prefix_second_name}")
        ValueError(f"No second name found in {composer_str} with prefix {prefix_second_name}")

    first_names.reverse()
    second_names.reverse()
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
            section_prefix = section_prefix.lower()
            for composer_string in composer_strings:
                composer_string = unidecode_except_german_umlaute(composer_string)
                composer_string = composer_string.lower()

                try:
                    match = re.fullmatch(COMPOSER_STRING_REGEX, composer_string)

                    first_name, second_name = get_first_second_name(
                                match.group("name"), section_prefix[:2])
                    geburts_jahr, todesjahr = get_geburts_todes_jahr(match.group("year"))
                    composers.append(
                        Composer(first_name, second_name, geburts_jahr, todesjahr, composer_string)
                    )
                except (ValueError, IndexError, AttributeError) as excp:
                    print(f"{composer_string}: {excp}")

    return composers


def get_composer_from_country():
    pass


def filter_composer_born_before(composer, year):
    if composer.geburtsjahr:
        return composer.geburtsjahr < year

    if composer.todesjahr:
        return composer.todesjahr - 10 < year

    return True


def test_get_composer(func):
    for composer in func():
        print(str(composer))


def get_composers_sorted() -> List[Composer]:
    composers = get_all_composers()
    composers = list(filter(lambda c: filter_composer_born_before(c, 1848), composers))

    composers = sorted(composers, key=lambda c: c.last_name)
    return composers


def store_composers_pickled(output_file):
    composers = get_all_composers()
    composers = list(filter(lambda c: filter_composer_born_before(c, 1848), composers))
    with open(output_file, "wb") as file:
        pickle.dump(composers, file)

