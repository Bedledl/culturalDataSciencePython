from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from data_mining import get_data_as_data_frame, get_rows, REL_FREQ_CSV_FILE

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


data = get_data_as_data_frame(REL_FREQ_CSV_FILE)
rows = get_rows(REL_FREQ_CSV_FILE)


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
    "Durchschnitt",

]
legende = [
    "A.M.Z. nicht erschienen",
    "Durchschnitt",
]
"""
most_frequent_mentioned_names = [
    "Durchschnitt",
    "Ferdinando Paer",
    "Wenzel Müller",
    "Wilhelm Schneider",
    "Ferdinand Hiller",
    "J N an Hummel",
    "s Friedrich Schneider",
    "Fr Melancholie Kalkbrenner",
    "Abts Vogler",
    "W A Oarert Mozart"
]

legende = [
    "A.M.Z. nicht erschienen",
    "Durchschnitt",
    "W. A. Mozart",
    "Ferdinando Paer, Spotify Popularity: 2",
    "Wenzel Müller, Spotify Popularity: 0",
    "Wilhelm Schneider, Spotify Popularity: 0",
    "Ferdinand (von) Hiller, Spotify Popularity: 4",
    "Johann Nepomuck Hummel, Spotify Popularity: 2",
    "Friedrich Schneider, Spotify Popularity: 3",
    "Friedrich Kalkbrenner, Spotify Popularity: 10",
    "Georg Joseph Vogler: 22"
]
"""
data = data.drop(["book"], axis=1)

data = data.pivot(index="year", columns="name", values="frequency")

print(data)
durchschnitt = data.mean(axis=1, skipna=True)
#durchschnitt.name = "Durchschnitt"
data.insert(0, "Durchschnitt", durchschnitt)
print(data)

data = data.fillna(0)
data = data.filter(items=most_frequent_mentioned_names)

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.1, top = 0.95, left=0.1, right=0.95) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Anteil der Namensnennungen')
plt.xlabel('Jahr')


print(data.columns)

def helper_top_frequ_chart(i: int):
    plt.legend(legende)
    if 1848 < i < 1863:
        p = plt.plot(data[:1849])
    elif i <= 1848:
        p = plt.plot(data[:i]) #note it only returns the dataset, up to the point i
    else:
        p = plt.plot(data[:1849] + data[1863:i])

    for i in range(0, min(len(p), 19)):
        p[i].set_color(color[i]) #set the colour of each curveimport matplotlib.animation as ani


animator = FuncAnimation(fig, helper_top_frequ_chart, frames=list(range(1799, 1849)) + list(range(1863, 1883)), interval=500)

plt.axvspan(1848, 1863, color='g', alpha=0.5, lw=0)
plt.show()
