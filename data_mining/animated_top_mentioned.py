import numpy as np
import matplotlib.pyplot as pltcolor
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from data_mining import get_names_most_frequent_mentioned_in_year, get_data_as_data_frame, get_rows, \
    get_names_most_frequent_mentioned_overall

color = [
    "#b96ba2",
    "#15e24c",
    "#98aae0",
    "#d45c08",
    "#8eb736",
    "#5511e3",
    "#b30248",
    "#82a518",
    "#46c526",
    "#288384",
    "#45cce8",
    "#f26acd",
    "#aca82e",
    "#6f907a",
    "#69f4e0",
    "#099438",
    "#1d6363",
    "#927bbf",
    "#02554e"
]
most_frequent_mentioned_names = set() # just names


data = get_data_as_data_frame()
rows = get_rows()

#for year in range(1799, 1849):
#    most_frequent_mentioned_year = get_names_most_frequent_mentioned_in_year(rows, year, 1)
#    for name in most_frequent_mentioned_year.keys():
#        most_frequent_mentioned_names.add(name)

most_frequent_mentioned_names = get_names_most_frequent_mentioned_overall(rows, 10)

print(len(most_frequent_mentioned_names))

print(most_frequent_mentioned_names)
most_frequent_mentioned_names = list(most_frequent_mentioned_names)

data = data.drop(["book"], axis=1)

#data.index = data["year"]
#data = data.groupby("year", group_keys=False, dropna=False)
#data = data.filter()

data = data.pivot(index="year", columns="name", values="frequency")
data = data.filter(items=most_frequent_mentioned_names)
data = data.fillna(0)

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.2, top = 0.9) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Erwähnungen')
plt.xlabel('Year')


def helper_top_frequ_chart(i: int):
    year = 1798 + i
    plt.legend(most_frequent_mentioned_names)
    p = plt.plot(data[:i]) #note it only returns the dataset, up to the point i
    for i in range(0, 10):
        p[i].set_color(color[i]) #set the colour of each curveimport matplotlib.animation as ani

animator = FuncAnimation(fig, helper_top_frequ_chart, interval = 500)
plt.show()
