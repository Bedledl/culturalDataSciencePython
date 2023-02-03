# berechne ähnlichkeiten zwischen Jahren auf Grundlage von Komponisten vektoren
# Ähnlichkeit wird durch Kosinusähnlichkeit brechnet

import math
from typing import Dict

import numpy
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering

from data_mining import get_data_as_data_frame, get_rows, \
    get_names_most_frequent_mentioned_overall, get_names_most_frequent_mentioned_in_year, sort_frequency_dict

IGNORE_NAMES = [
    "Don Juan", # Protagonist
    "GC W Fink", # Verleger
                ]

data = get_data_as_data_frame()
rows = get_rows()

most_frequent_mentioned_names = set()

for year in range(1799, 1849):
    most_frequent_mentioned_year = get_names_most_frequent_mentioned_in_year(rows, year, 25)
    for name in most_frequent_mentioned_year.keys():
        most_frequent_mentioned_names.add(name)

for year in range(1863, 1883):
    most_frequent_mentioned_year = get_names_most_frequent_mentioned_in_year(rows, year, 25)
    for name in most_frequent_mentioned_year.keys():
        most_frequent_mentioned_names.add(name)

print(len(most_frequent_mentioned_names))

print(most_frequent_mentioned_names)
most_frequent_mentioned_names = list(most_frequent_mentioned_names)
for i_name in IGNORE_NAMES:
    try:
        most_frequent_mentioned_names.remove(i_name)
    except ValueError:
        pass

data = data.drop(["book"], axis=1)

data = data.pivot(index="year", columns="name", values="frequency")
data = data.filter(items=most_frequent_mentioned_names)
data = data.fillna(0)

#print(data.apply(lambda x: x.apply(math.log2) if type(x) == pd.Series else x))
#print(data)
#print(data.apply(numpy.log2))

indecies = list(data.columns)
record = pd.DataFrame.to_records(data, index=False, column_dtypes=None, index_dtypes=None)
record_with_index = pd.DataFrame.to_records(data, index=True, column_dtypes=None, index_dtypes=None)

row_labels = [r[0] for r in record_with_index]

#record = numpy.array([[math.log2(x) if x > 1 else x for x in row] for row in record])
#record = numpy.array([[x/sum(row) * 1000 for x in row] for row in record])
record = numpy.array([[x/sum(row) * 1000 for i, x in enumerate(row)] for row in record])


clustering = AgglomerativeClustering(n_clusters=10, affinity='cosine',
                        memory=None, connectivity=None, compute_full_tree='auto',
                        linkage='single', distance_threshold=None, compute_distances=False)

#clustering.labels_ = row_labels
#print(clustering.labels_)
result = clustering.fit_predict(record)
print(result)


class Cluster:
    def __init__(self):
        self.years = []
        self.namen_frequencies = {}

    def get_sorted_namen_frequencies(self):
        return sort_frequency_dict(self.namen_frequencies)

    def print(self):
        print(f"In den Jahren {', '.join([str(y) for y in self.years])} folgende Namen wurden am häufigsten genannt")
        frequencies = self.get_sorted_namen_frequencies()
        print(frequencies)

    def update_frequencies(self, name_frequency_dict: Dict[str, int]):
        for name, freq in name_frequency_dict.items():
            if name in self.namen_frequencies.keys():
                self.namen_frequencies[name] += freq

            else:
                self.namen_frequencies[name] = freq


clusters = [Cluster() for _ in range(10)]

for i, cluster_nr in enumerate(result):
    clusters[cluster_nr].years.append(row_labels[i])

for cluster in clusters:
    for year in cluster.years:
        names = get_names_most_frequent_mentioned_in_year(rows, year, 25)
        d = {
            name: record[row_labels.index(year)][indecies.index(name)]for name in names
        }
        cluster.update_frequencies(d)

    cluster.print()
