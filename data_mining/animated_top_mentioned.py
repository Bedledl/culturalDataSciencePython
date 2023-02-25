import numpy as np
import matplotlib.pyplot as pltcolor
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from data_mining import get_names_most_frequent_mentioned_in_year, get_data_as_data_frame, get_rows, \
    get_names_most_frequent_mentioned_overall

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
most_frequent_mentioned_names = set() # just names


data = get_data_as_data_frame()
rows = get_rows()

#for year in range(1799, 1849):
#    most_frequent_mentioned_year = get_names_most_frequent_mentioned_in_year(rows, year, 3)
#    for name in most_frequent_mentioned_year.keys():
#        most_frequent_mentioned_names.add(name)
"""
most_frequent_mentioned_names = get_names_most_frequent_mentioned_overall(rows, 1000)

print(len(most_frequent_mentioned_names))

print(most_frequent_mentioned_names)
most_frequent_mentioned_names = list(most_frequent_mentioned_names)
for i_name in IGNORE_NAMES:
    try:
        most_frequent_mentioned_names.remove(i_name)
    except ValueError:
        pass
"""
most_frequent_mentioned_names = [
    "Johann Sebastian Bach",
    "W A Oarert Mozart",
    "SINFONIEN Beethoven",
    "Joseph I Haydn",
    "Dr Klara Schumann"
]
data = data.drop(["book"], axis=1)

#data.index = data["year"]
#data = data.groupby("year", group_keys=False, dropna=False)
#data = data.filter()

data = data.pivot(index="year", columns="name", values="frequency")
data = data.filter(items=most_frequent_mentioned_names)
data = data.fillna(0)

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.1, top = 0.95, left=0.1, right=0.95) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Erwähnungen')
plt.xlabel('Year')


def helper_top_frequ_chart(i: int):
    year = 1798 + i
    plt.legend(most_frequent_mentioned_names)
    p = plt.plot(data[:i]) #note it only returns the dataset, up to the point i
    for i in range(0, min(len(p), 19)):
        p[i].set_color(color[i]) #set the colour of each curveimport matplotlib.animation as ani

animator = FuncAnimation(fig, helper_top_frequ_chart, interval = 500)
plt.show()
