import csv

import pandas as pd
import functools
from typing import Dict

CSV_FILE = "../frequency_without_linking/entity_freq_1_2_whole.csv"


def get_data_as_data_frame() -> pd.DataFrame:
    return pd.read_csv(CSV_FILE, delimiter=',', header=0)


def get_rows():
    with open(CSV_FILE) as csvfile:
        spamreader = csv.reader(csvfile)

        spamreader.__next__()

        data = []
        for row in spamreader:
            data.append(row)
    return data


def get_sums_mentions(data, year: int = None):
    # input is read csv
    # output row for each name: [name,,(first,last),frequency] e.g. [Müller,,(1834,148),59]
    freq_dict = {}
    for row in data:
        if year and int(row[2]) != year:
            continue

        name = row[0]
        freq = int(row[3])
        if name not in freq_dict.keys():
            freq_dict[name] = freq

        else:
            freq_dict[name] += freq

    return freq_dict


def sort_frequency_dict(frequency_dict: Dict[str, int]):
    return dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True))


def get_names_most_frequent_mentioned(frequency_dict_sorted: Dict[str, int], n: int):
    # input frequency dict from sort_frequency_dict und get_sum_mentions
    # return dictionary out of names and frequency
    return_dict = {}
    for i, items in enumerate(frequency_dict_sorted.items()):
        if i == n:
            break

        return_dict[items[0]] = items[1]

    return return_dict


def get_names_most_frequent_mentioned_in_year(data, year, n):
    '''
    find the n most frequent mentioned names in year.
    '''
    frequency_dict = get_sums_mentions(data, year)
    frequency_dict_sorted = sort_frequency_dict(frequency_dict)
    return get_names_most_frequent_mentioned(frequency_dict_sorted, n)


def get_names_most_frequent_mentioned_overall(data, n):
    frequency_dict = get_sums_mentions(data)
    frequency_dict_sorted = sort_frequency_dict(frequency_dict)
    return get_names_most_frequent_mentioned(frequency_dict_sorted, n)


