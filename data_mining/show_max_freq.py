from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd

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
    "W A Oarert Mozart",
    "Ferdinando Paer",
    "Wenzel Müller",
    "Wilhelm Schneider",
    "Ferdinand Hiller",
    "J N an Hummel",
    "s Friedrich Schneider",
    "Fr Melancholie Kalkbrenner",
    "Abts Vogler"
]

legende = [
    "A.M.Z. nicht erschienen",
    "Durchschnitt",
    "W. A. Mozart",
    "Ferdinando Paer",
    "Wenzel Müller",
    "Wilhelm Schneider",
    "Ferdinand (von) Hiller",
    "Johann Nepomuck Hummel",
    "Friedrich Schneider",
    "Friedrich Kalkbrenner",
    "Georg Joseph Vogler"
]

spotify_pop_dict = {
    "W A Oarert Mozart": 77,
    "Ferdinando Paer": 2,
    "Wenzel Müller": 0,
    "Wilhelm Schneider": 0,
    "Ferdinand Hiller": 4,
    "J N an Hummel": 2,
    "s Friedrich Schneider": 3,
    "Fr Melancholie Kalkbrenner": 10,
    "Abts Vogler": 22
}


data = data.drop(["book"], axis=1)

data = data.pivot(index="year", columns="name", values="frequency")

print(data)
durchschnitt = data.mean(axis=1, skipna=True)
#durchschnitt.name = "Durchschnitt"
data.insert(0, "Durchschnitt", durchschnitt)

data = data.fillna(0)
data = data.filter(items=most_frequent_mentioned_names)

fig = plt.figure()
plt.xticks(rotation=45, ha="right", rotation_mode="anchor") #rotate the x-axis values
plt.subplots_adjust(bottom = 0.1, top = 0.95, left=0.1, right=0.95) #ensuring the dates (on the x-axis) fit in the screen
plt.ylabel('Anteil der Namensnennungen')
plt.xlabel('Jahr')

plt.axvspan(1848, 1863, color='g', alpha=0.5, lw=0)
plt.plot(data["Durchschnitt"])
plt.plot(data["W A Oarert Mozart"])

print("Max Values")
max_ids = data.idxmax()
print(max_ids)
max_data = data.max(axis=0)
max_values = pd.DataFrame(max_data, columns=["max_value"], index=max_data.index)
max_values.insert(1, "year", max_ids)
max_values = max_values.drop("Durchschnitt")
max_values = max_values.drop("W A Oarert Mozart")

for name, max_value, year in max_values.to_records():
    plt.scatter(year, max_value, 10 + 10 * spotify_pop_dict[name])
    plt.text(year, max_value, spotify_pop_dict[name], horizontalalignment='center', verticalalignment='center', fontsize="x-large")

#plt.scatter(max_values)
plt.legend(legende)

plt.show()
