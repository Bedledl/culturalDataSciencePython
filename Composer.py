import re
from typing import List, Dict

NAME_MATCHING_REGEX = "{name}(s|i?sche(s|n|r)?)?"


class Composer:
    def __init__(self, first_name: str, last_name: str, geburtsjahr: int, todesjahr: int, original_string=""):
        if not last_name:
            raise ValueError(f"No last name is given {original_string}.")
        self.first_name = first_name
        self.last_name = last_name.capitalize()
        self.geburtsjahr = geburtsjahr
        self.todesjahr = todesjahr
        self.frequencies = {}
        self.__name_match_regex = re.compile(NAME_MATCHING_REGEX.format(name=self.last_name))
        self.__len_last_name = len(self.last_name)
        self.spotify_id = None
        self.spotify_popularity = 0
        self.spotify_followers = 0
        self.false_positive_rate = 0

        self.original_string = original_string if original_string else first_name + " " + last_name

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

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    def increment_frequency_in(self, article_key: str):

        try:
            self.frequencies[article_key] = self.frequencies[article_key] + 1
        except KeyError:
            self.frequencies[article_key] = 1

    def name_pattern_combinations(self) -> List[List[Dict[str, str]]]:
        combinations = []
        # nur nachname
        pattern = [{"LOWER": self.last_name}]
        combinations.append(pattern)

        pattern = [{"LOWER": self.last_name + ","}]
        combinations.append(pattern)

        if not self.first_name:
            return combinations

        # vornamen
        vornamen = []
        for vorname in self.first_name.split():
            vornamen.append(vorname)
            pattern = [{"LOWER": name} for name in vornamen] + [{"LOWER": self.last_name}]
            combinations.append(pattern)
        # vornamen abkürzungen
        vornamen = []
        for vorname in self.first_name.split():
            vornamen.append(vorname[0])

            # W A Mozart
            pattern = [{"LOWER": name} for name in vornamen] + [{"LOWER": self.last_name}]
            combinations.append(pattern)

            # W.A. Mozart
            pattern = []
            for name in vornamen:
                pattern += [{"LOWER": name + "."}]

            pattern += [{"LOWER": self.last_name}]
            combinations.append(pattern)

            # Mozart, W.A.
            pattern = [{"LOWER": self.last_name}]
            for name in vornamen:
                pattern += [{"LOWER": name + "."}]

            combinations.append(pattern)

        return combinations


class Nachname:
    def __init__(self, name: str):
        self.name = name
        self.ref_composers = []

    def match(self, search_str: str):
        search_str = search_str.strip(".,")
        name_splitted = search_str.split()
        second_name = name_splitted[-1]
        if self.name not in second_name:
            return False

        for composer in self.ref_composers:
            if composer.match(search_str) == 0:
                return True

        return False
    from Levenshtein import apply_edit
