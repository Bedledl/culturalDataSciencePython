import csv

import pandas as pd
import functools
from typing import Dict

CSV_FILE = "../frequency_without_linking/entity_freq_1_2_whole.csv"
REL_FREQ_CSV_FILE = "../frequency_without_linking/rel_freq_6_2.csv"


def get_data_as_data_frame(input_file) -> pd.DataFrame:
    return pd.read_csv(input_file, delimiter=',', header=0)


def get_rows(input_file):
    with open(input_file) as csvfile:
        spamreader = csv.reader(csvfile)

        spamreader.__next__()

        data = []
        for row in spamreader:
            data.append(row)
    return data


def get_sums_mentions(data, year: int = None):
    # input is read csv as [(name, book, year, freq), ...]
    # output row for each name: {"name": freq: int}
    freq_dict = {}
    for row in data:
        if year and int(row[2]) != year:
            continue

        name = row[0]
        freq = float(row[3])
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


def get_names_most_frequent_mentioned_in_year(data, year, n):
    '''
    find the n most frequent mentioned names in year.
    '''
    frequency_dict = get_sums_mentions(data, year)
    frequency_dict_sorted = sort_frequency_dict(frequency_dict)
    return get_names_most_frequent_mentioned(frequency_dict_sorted, n)

#rows = get_rows()
#print(get_names_most_frequent_mentioned_in_year(rows, 1882, 50))


def get_relative_freq(input_file, output_file):
    output_rows = []
    rows = get_rows(input_file)
    year_frequ_dict = {str(year): 0 for year in list(range(1799, 1849)) + list(range(1863, 1883))}
    for row in rows:
        year_frequ_dict[row[2]] += int(row[3])

    for row in rows:
        freq = int(row[3])/year_frequ_dict[row[2]] * 100
        row_new = (row[0], row[1], row[2], str(freq))
        output_rows.append(row_new)

    header = ["name", "book", "year", "frequency"]

    csv_file = open(output_file, "w")
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(header)
    csv_writer.writerows(output_rows)

#get_relative_freq(CSV_FILE, REL_FREQ_CSV_FILE)