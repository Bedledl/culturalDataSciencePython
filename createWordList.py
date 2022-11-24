import csv
import pickle
import re
from typing import List

from helper import unidecode_except_german_umlaute
from wikipediaClassicalComposersProxy import get_all_composers, filter_composer_born_before, Composer

from processGeneratedTextFile import preprocess_text_file
from Log import log

OUTPUT_FILE = "frequencies1-16.csv"
#input_files = [f"AMZ{i}.txt" for i in range(1, 17)]
INPUT_FILES = [f"AMZ{i}.txt" for i in range(1, 17)]


def get_pickled_composers(pickle_file_name: str):
    with open(pickle_file_name, "rb") as file:
        composers = pickle.load(file)
    return composers

#
# for every input file a row in the csv is created
# for every word a column is crated
#


def find_matches_and_increment(text, composers: List[Composer], filename: str):
    line_words = text.split()

    for word in line_words:

        for composer in composers:
            cmp = composer.match(word)
            if cmp == 0:
                composer.increment_frequency_in(filename)
            elif cmp > 0:
                break


def update_frequencies_in_composers(composers: List[Composer], input_files):
    for input_file_name in input_files:
        log(f"Open and preprocess {input_file_name}")
        preprocessed_text_file = "pre-" + input_file_name

        preprocess_text_file(input_file_name, preprocessed_text_file)
        log("Preprocessed")

        with open(preprocessed_text_file) as input_file:
            for line in input_file:
                find_matches_and_increment(line, composers, input_file_name)


def create_frequency_file(composers: List[Composer], input_files, output_file):
    header = ["name", "book", "year", "frequency"]

    csv_file = open(output_file, "w")
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(header)

    update_frequencies_in_composers(composers, input_files)

    log("Now Write to File:")
    last_name_written = ""
    for composer in composers:
        if sum(composer.frequencies.values()) == 0:
            continue

        if last_name_written == composer.last_name:
            continue
        last_name_written = composer.last_name

        for book, frequency in composer.frequencies.items():
            year = str(int(book[3:-4]) + 1798)
            print(year)
            csv_writer.writerow([composer.short, book, year, frequency])

    csv_file.close()


def create_frequency_file_spotify(composers: List[Composer], input_files, output_file):
    header = ["name", "frequency_amz", "spotify_popularity", "spotify_follower"]

    csv_file = open(output_file, "w")
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(header)

    update_frequencies_in_composers(composers, input_files)

    log("Now Write to File:")

    for composer in composers:
        frequency_amz = sum(composer.frequencies.values())

        csv_writer.writerow([composer.name, frequency_amz, composer.spotify_popularity, composer.spotify_followers])

    csv_file.close()


def get_environments_of_componist_mention(text: str, composer: Composer, environment_size: int):
    environments = []
    text_split = text.split()
    for index, word in enumerate(text_split):
        if composer.match(word) != 0:
            continue

        environment = text_split[index - environment_size: index + environment_size + 1]
        environments.append(" ".join(environment))

    return environments


def test_envrionment_of_componsit():
    bach = Composer("", "Ruhe", 1666, 1723)
    with open("AMZ1.txt", "r") as file:
        text = file.read()

    with open("AMZ2.txt", "r") as file:
        text += file.read()

    with open("AMZ14.txt", "r") as file:
        text += file.read()

    with open("AMZ22.txt", "r") as file:
        text += file.read()

    text = unidecode_except_german_umlaute(text)
    text = re.sub("[\*\.,;:-]", " ", text)

    e1 = get_environments_of_componist_mention(text, bach, 4)
    for e in e1:
        print(e)


#test_envrionment_of_componsit()
#reate_frequency_file(get_composers_sorted(), input_files, output_file)

#print("Start:")
#composers = get_pickled_composers("composers_spotify.dat")
#INPUT_FILES = [f"AMZ{i}.txt" for i in range(1, 3)]
#print("Start generating frequency file:")
#create_frequency_file_spotify(composers, INPUT_FILES, "frequency_spotify_draft.csv")