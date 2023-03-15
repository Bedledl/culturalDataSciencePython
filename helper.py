"""
file for helper functions
"""
from unidecode import unidecode

def unidecode_except_german_umlaute(string: str) -> str:
    result = ""
    tmp = ""
    for char in string:
        if ord(char) > 383:
            tmp += char
        else:
            result += unidecode(tmp) + char
            tmp = ""

    result += tmp
    return result
