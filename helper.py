"""
file for helper functions
"""
from unidecode import unidecode

GERMAN_UMLAUTE = ['ä', 'ö', 'ü', 'Ä', 'Ö', 'Ü', 'ß']


def unidecode_except_german_umlaute(string: str) -> str:
    result = ""
    tmp = ""
    for char in string:
        if char not in GERMAN_UMLAUTE:
            tmp += char
        else:
            result += unidecode(tmp) + char
            tmp = ""

    result += tmp
    return result
