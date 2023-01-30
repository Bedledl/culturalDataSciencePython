import csv
import pickle
from typing import List

from Levenshtein import ratio, distance
from rapidfuzz.string_metric import levenshtein

from Composer import Composer

COMPOSER_FILE = "composers_spotify.dat"


def find_composer_match(composers: List[Composer], search_string: str, threshold: int):
    best_match = None
    best_match_ratio = 0
    for composer in composers:
        r = ratio(composer.last_name, search_string)
        if r >= threshold and r > best_match_ratio:
            best_match = composer
            best_match_ratio = r

    return best_match


def find_composer_match_(composers: List[Composer], search_string: str):
    best_match = None
    best_match_distance = 5 * len(search_string)
    for composer in composers:
        r = distance(composer.last_name, search_string, weights=(1, 3, 2))
        if r < best_match_distance:
            best_match = composer
            best_match_distance = r

    return best_match


def create_frequency_dict(input_doc_file: str, composers: List[Composer]):
    freq_dict = {}

    with open(input_doc_file, "rb") as file:
        doc = pickle.load(file)[0]

    for ent in doc.ents:
        if ent.label_ != "PER":
            continue
        print(ent.text)

    for ent in doc.ents:
        if ent.label_ != "PER":
            continue

        best_match = find_composer_match(composers, ent.text, 0.5)
        #best_match = find_composer_match(composers, ent.text)

        if not best_match:
            print(f"{ent.text} not matched")
            continue

        print(f"matched {ent.text} with {best_match.name}")

        try:
            freq_dict[best_match.name] = freq_dict[best_match.name] + 1
        except KeyError:
            freq_dict[best_match.name] = 1

    return freq_dict


with open(COMPOSER_FILE, "rb") as file:
    composers = pickle.load(file)

header = ["name", "book", "year", "frequency"]

csv_file = open("entity_freq_29_1.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(header)

#for i in range(1, 51):
for i in range(1, 3):
    year = 1798
    file_name_dat = f"/mnt/sdb1/cds/data/entities_files/AMZ_wmodel{i}.dat"

    freq_dict = create_frequency_dict(file_name_dat, composers)
    for name, freq in freq_dict.items():
        csv_writer.writerow([name, "AMZ" + str(year + i), str(year + i), freq])

csv_file.close()

