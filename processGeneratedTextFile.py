
#text_file = "data/AMZ1799.txt"
#input_text_file = "test.txt"
#output_text_file = "test_pretty.txt"
#output_text_file = "data/AMZ1799_pretty.txt"
from helper import unidecode_except_german_umlaute

SIZE_GOOGLE_HEADER = 3750
import re

from Log import log


def strip_google_header(text: str) -> str:
    return text[SIZE_GOOGLE_HEADER:]


def zeilenumbrueche_entfernen(text: str) -> str:
    return re.sub("-\n", " ", text)


def preprocess_text_file(input_text_file, output_text_file):
    with open(input_text_file, "r") as file:
        text = file.read()
        text = unidecode_except_german_umlaute(text)
        #text = strip_google_header(text)
        text = zeilenumbrueche_entfernen(text)
        #text = re.sub("[\*\.,;:-]", " ", text)
        log("Now writing processed:")
        with open(output_text_file, "w") as file:
            file.write(text)


def preprocess_text(text: str):
    text = strip_google_header(text)
    text = unidecode_except_german_umlaute(text)
    text = zeilenumbrueche_entfernen(text)
