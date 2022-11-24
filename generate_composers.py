'''
This script creates a pickled composer file.
This script handles:
- spotify information
- AMZ frequency information
- redundant surename behaviour
- false positive approximation
'''
import random

import spotipy

from false_positive_approximation import find_false_positive_rate
from processSpotifyComposers import add_spotify_infos_to_composers
from wikipediaClassicalComposersProxy import get_composers_sorted
import hunspell

AMZ_INPUT_FILES = [f"AMZ{i}.txt" for i in range(1, 3)]

hunspell_obj = hunspell.HunSpell("/usr/share/hunspell/de_DE.dic", "/usr/share/hunspell/de_DE.aff")
conn = spotipy.Spotify(client_credentials_manager=spotipy.SpotifyClientCredentials())

# fetch composers from Wikipedia, filter out everyone born after 1848 and sort them
composers = get_composers_sorted()

# only for testing purposes
composers = random.sample(composers, 100)

print(f"get_composers_sorted: {len(composers)}")

composers = add_spotify_infos_to_composers(conn, composers)

print(f"after Spotify filtering: {len(composers)}")

for composer in composers:
    if hunspell_obj.spell(composer.last_name):
        fpr = find_false_positive_rate(composer, AMZ_INPUT_FILES, 10)
        print(f"composer {composer.name} has fpr: {fpr}")


