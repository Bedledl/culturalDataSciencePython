'''
this file provides method to handle multiple componists with the same name
'''
from random import random
from typing import List

from Composer import Composer
from createWordList import get_environments_of_componist_mention


def get_redundant_composers(composers: List[Composer]):
    name_dict = {}
    for composer in composers:
        try:
            name_dict[composer.last_name].append(composer)
        except KeyError:
            name_dict[composer.last_name] = [composer]

    return {name: list for name, c_list in name_dict.items() if len(c_list) > 1}


def handle_redundant_composers(composers: List[Composer], input_files: List[str], test_size: int):
    text = ""
    environments = []

    for file in input_files:
        with open(file, "r") as input_file:
            text += input_file.read()

    composers = get_redundant_composers(composers)

    for name, composer_list in composers.items():
        environments.append(get_environments_of_componist_mention(text, composer_list[0], 5))

        try:
            environments = random.sample(environments, test_size * len(composer_list))
        except ValueError:
            pass

        composer_nr_ass = dict(enumerate(composer_list))
        rates = {i: 0 for i in composer_nr_ass.keys()}
        unknown = 0

        print(f"{name}:")
        for i, composer in composer_nr_ass.items():
            print(f"    {i} : {composer.first_name}")

        for sentence in environments:
            answer = ""
            while answer not in [str(k) for k in rates.keys()] + ["n"]:
                answer = input(f"{sentence}")

            if answer == "n":
                unknown += 1

            else:
                rates[int(answer)] += 1

        return false_positives / len(environments)
