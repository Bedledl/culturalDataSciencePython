
#text_file = "data/AMZ1799.txt"
#input_text_file = "test.txt"
#output_text_file = "test_pretty.txt"
#output_text_file = "data/AMZ1799_pretty.txt"
from helper import unidecode_except_german_umlaute

SIZE_GOOGLE_HEADER = 3760
import re

from Log import log


def strip_google_header(text: str) -> str:
    index = text.find("ALLGEMEINE")
    diff = abs(SIZE_GOOGLE_HEADER - index)
    if diff > 50:
        raise ValueError("'ALLGEMEINE' not found at the usual index.")

    return text[index:]


def zeilenumbrueche_entfernen(text: str) -> str:
    return re.sub("-\n", " ", text)


def preprocess_text_file(input_text_file, output_text_file):
    with open(input_text_file, "r") as file:
        text = file.read()
        text = unidecode_except_german_umlaute(text)
        #text = strip_google_header(text)
        text = zeilenumbrueche_entfernen(text)
        text = re.sub("[\*\.,;:-]", " ", text)
        log("Now writing processed:")
        with open(output_text_file, "w") as file:
            file.write(text)
