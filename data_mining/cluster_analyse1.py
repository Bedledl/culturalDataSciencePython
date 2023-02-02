from data_mining import get_data_as_data_frame, get_rows, \
    get_names_most_frequent_mentioned_overall

IGNORE_NAMES = [
    "Don Juan", # Protagonist
    "GC W Fink", # Verleger
                ]

data = get_data_as_data_frame()
rows = get_rows()

most_frequent_mentioned_names = get_names_most_frequent_mentioned_overall(rows, 500)

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

print(data)