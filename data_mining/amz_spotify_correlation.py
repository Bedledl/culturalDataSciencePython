import math
from statistics import variance

import numpy as np
import matplotlib.pyplot as pltcolor
import pandas as pd
import spotipy
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import mean, median, sqrt
from spotipy import SpotifyClientCredentials

from data_mining import get_names_most_frequent_mentioned_in_year, get_data_as_data_frame, get_rows, \
    get_names_most_frequent_mentioned_overall, REL_FREQ_CSV_FILE
from helper import unidecode_except_german_umlaute
from spotifyProxy import get_componist_search_results, get_composer_props, ComposerProps

color = [
    "#FF0000",
    "#00FF00",
    "#0000FF",
    "#FFFF00",
    "#00FFFF",
    "#FF00FF",
    "#C0C0C0",
    "#808080",
    "#800000",
    "#808000",
    "#008000",
    "#800080",
    "#008080",
    "#FA8072",
    "#00FA9A",
    "#6495ED",
    "#87CEFA",
    "#FAEBD7",
    "#D2691E"
]

IGNORE_NAMES = [
    "Don Juan", # Protagonist
    "GC W Fink", # Verleger
                ]

data = get_data_as_data_frame(REL_FREQ_CSV_FILE)
rows = get_rows(REL_FREQ_CSV_FILE)

#for year in range(1799, 1849):
#    most_frequent_mentioned_year = get_names_most_frequent_mentioned_in_year(rows, year, 3)
#    for name in most_frequent_mentioned_year.keys():
#        most_frequent_mentioned_names.add(name)

# es gibt insgesamt 20974

most_frequent_mentioned_names = {name: freq for name, freq in get_names_most_frequent_mentioned_overall(rows, 1000).items()}


for i_name in IGNORE_NAMES:
    try:
        most_frequent_mentioned_names.pop(i_name)
    except KeyError:
        pass

#data = data.drop(["book"], axis=1)

#data.index = data["year"]
#data = data.groupby("year", group_keys=False, dropna=False)
#data = data.filter()

data = data.pivot(index="year", columns="name", values="frequency")
data = data.filter(items=most_frequent_mentioned_names)
data = data.fillna(0)

data_sum = {person: data[person].sum() for person in data.columns}

print(data_sum)
# frequenzen der Künstler sind ziemlich exponentiell "wachsend" deshalb logarithmus zum normalisieren

data_sum = {name: math.log2(freq) for name, freq in data_sum.items()}

print(data_sum)
max_ = max(data_sum.values())
min_ = min(data_sum.values())
#Median = median(list(data_sum.values()))
#mittlere_absolute_Abweichung_Median = 1.0/len(data_sum) * sum([abs(n-Median) for n in data_sum.values()])

Mean = mean(list(data_sum.values()))
mittlere_absolute_Abweichung = sqrt(variance(list(data_sum.values())))

print(Mean)
print(mittlere_absolute_Abweichung)


def z_transformation(x, m, mittlereabweichung):
    return (x - m)/mittlereabweichung


def min_max_transformation(x, min_, max_):
    return int((x - min_) / (max_ - min_) * 100)

popularity_dict = {name: min_max_transformation(i, min_, max_) for name, i in data_sum.items()}
#print([z_transformation(i, Mean, mittlere_absolute_Abweichung) for i in data_sum.values()])

conn = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="e0f913cf7ae4441dab30a2adf5624842",
                                                             client_secret="0c4754573c64405ead446f0acd861650"))

print("Connected:)")
result = conn.search("Georg Joseph Vogler", type="artist")["artists"]["items"][0]
print(result)
r_uri, r_name = result["uri"], result["name"]
print(r_name)
props = get_composer_props(conn, r_uri,
                                       [ComposerProps.POPULARITY])
spotify_popularity = props[ComposerProps.POPULARITY]
print(spotify_popularity)
print("now")


def get_nachname(name):
    split = name.split()
    return split[-1]


popularity_dif = {}


for name, popularity in popularity_dict.items():
    if popularity < 20:
        continue

    try:
        results = get_componist_search_results(conn, name)
    except TimeoutError:
        print(f"Timeout Error for {name}")
    if len(results) == 0:
        print(f"Keine Ergebnisse(amz popularity {popularity}): {name}")
    for result_uri, result_name in results.items():
        if unidecode_except_german_umlaute(get_nachname(result_name).lower()) \
                == unidecode_except_german_umlaute(get_nachname(name.lower())):
            props = get_composer_props(conn, result_uri,
                                       [ComposerProps.POPULARITY])
            spotify_popularity = props[ComposerProps.POPULARITY]
            print(f"{name}, {result_name}: amz popularity: {popularity} vs. spotify popularity {spotify_popularity}")
            popularity_dif[name] = popularity - spotify_popularity
            break

print(sorted(popularity_dif.items(), key=lambda x: x[1]))
