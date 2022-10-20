import csv
from getComposers import get_all_composers

output_file = "frequencies1799.csv"
input_files = ["AMZ1.txt", "AMZ2.txt"]

#key_words = ["Mozart", "Beethoven", "Bach", "Weber", "Wagner", "Haydn"]
key_words = list(set([composer.last_name for composer in get_all_composers()]))
print(len(key_words))
#
# for every input file a row in the csv is created
# for every word a column is crated
#


header = ["name"] + key_words

csv_file = open(output_file, "w")
csv_writer = csv.writer(csv_file)

csv_writer.writerow(header)

for input_file_name in input_files:
    frequency_dict = {word: 0 for word in key_words}

    with open(input_file_name) as input_file:
        for line in input_file:
            line_words = line.split()
            for word in line_words:
                for key_word in key_words:
                    if key_word in word:
                        frequency_dict[key_word] = frequency_dict[key_word] + 1

    csv_writer.writerow([input_file_name] + list(frequency_dict.values()))

csv_file.close()
