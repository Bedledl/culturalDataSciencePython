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

NAME_MATCHING_REGEX = "{name}(s|i?sche(s|n|r)?)?"
PREFIX_NAME_MATCHING_REGEX = "([LDd]')?{prefix}"
COMPOSER_STRING_REGEX = "(?P<name>[^\(\)]*) ?(\([^\(\)]*\))? ?\((?P<year>[^\(\)]*)\)"

'''
def number_to_base(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def get_character_list():
    char_list = [chr(i) for i in range(ord("a"), ord("z")+1)]
    return char_list


def lower_string_to_number(string):
    char_list = get_character_list()
    base = len(char_list) - 1
    num = 0
    for index, char in enumerate(string[::-1]):
        num += (base**index) * char_list.index(char)

    return num


def number_to_lower_string(num):
    char_list = get_character_list()
    base = len(char_list) - 1

    index_list = number_to_base(num, base)
    return "".join([char_list[index] for index in index_list])


def get_prefix_range(prefix_str):
    """
    Get list of possible prefixes from prefix strings like "Do" or "Dem-Dez"
    """
    if "-" not in prefix_str:
        return [prefix_str]

    if len(prefix_split := prefix_str.split("-")) != 2:
        raise ValueError(f"Could not extract prefix range from {prefix_str}")

    if len(prefix_split[0]) != len(prefix_split[1]):
        raise ValueError(f"Prefixes have various length! {prefix_str}")

    prefix_list = []
    for num in range(lower_string_to_number(prefix_split[0]), lower_string_to_number(prefix_split[1]) + 1):
        prefix = number_to_lower_string(num)
        prefix = prefix.capitalize()
        prefix_list.append(prefix)

    return prefix_list
    
'''


class Composer:
    def __init__(self, first_name: str, last_name: str, geburtsjahr: int, todesjahr: int, original_string=""):
        if not last_name:
            raise ValueError(f"No last name is given {original_string}.")
        self.first_name = first_name
        self.last_name = last_name.capitalize()
        self.geburtsjahr = geburtsjahr
        self.todesjahr = todesjahr
        self.original_str = original_string
        self.frequencies = {}
        self.__name_match_regex = re.compile(NAME_MATCHING_REGEX.format(name=self.last_name))
        self.__len_last_name = len(self.last_name)

    def __str__(self):
        return f"Last_Name{self.last_name} FirstName: {self.first_name} {self.geburtsjahr} {self.todesjahr}"

    def match(self, word: str) -> int:
        '''

        :param word: word to match with the name of the composer
        :return: 0 if the word matches
            > 0 if the word is smaller than the name
            < 0 if the word is greater than the name
        '''
        if len(word) >= self.__len_last_name:
            if self.__name_match_regex.fullmatch(word):
                return 0

        cmp = word < self.last_name
        if cmp:
            return 1
        else:
            return -1



    @property
    def short(self):
        return self.last_name
        if self.original_string:
            return self.original_str

        return self.first_name + self.last_name

    def initiate_frequencies_dict(self, article_keys):
        for a_key in article_keys:
            self.frequencies[a_key] = 0

    def increment_frequency_in(self, article_key: str):
        self.frequencies[article_key] = self.frequencies[article_key] + 1


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
                composer_string = unidecode(composer_string)
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

#test_get_composer(get_all_composers)