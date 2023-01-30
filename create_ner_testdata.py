# add # parenthesis around names
#"ner_test_short"
import re


def create_ner_testdata(input_file: str):
    with open(input_file, "r") as test_ner:
        test_text = test_ner.read()

    ents = []

    text = ""
    i = 0
    entity = False
    current_start = None
    for char in test_text:
        if char == "#":
            if not entity:
                current_start = i
                entity = True
            else:
                ents.append((current_start, i))
                entity = False
        else:
            text += char
            i += 1
    return ents


#with open("ner_test_ents") as file:
#    text = file.read()
#    text = re.sub("#", "", text)
#
#for begin, end in create_ner_testdata("ner_test_ents"):
#    print(text[begin: end])
