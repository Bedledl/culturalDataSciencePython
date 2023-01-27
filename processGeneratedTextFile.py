
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

substitute = {
    "(?P<stabe>\w)-\n": "\g<stabe>",
    "(\n[^a-zA-Z]*)\n": "\n",
    "\n\n": "\n",
    "\n\w{0,3}\n": "\n",
    "(?P<notDot>[^\.])\n(?P<under>[^A-Z])": "\g<notDot> \g<under>"
#    "[^\.]\n": " "
}


def zeilenumbrueche_entfernen(text: str) -> str:
    for s, ss in substitute.items():
        text = re.sub(s, ss, text)

    return text


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


for number in range(1, 51):
    preprocess_text_file(f"AMZ_wmodel{number}.txt", f"AMZ_wmodel{number}_preprocessed.txt")

#preprocess_text_file("data/ner_checkdata/ner_test", "data/ner_checkdata/ner_test_preprocessed")
