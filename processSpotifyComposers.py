'''
This script takes a pickled list of composers and tries to match every composer with its spotify
'''
import pickle
from typing import List

import spotipy
from spotipy import SpotifyClientCredentials, Spotify

from Composer import Composer
from helper import unidecode_except_german_umlaute
from spotifyProxy import get_componist_search_results, ComposerProps, get_composer_props

INPUT_FILE = "composers_pickled.dat"
OUTPUT_FILE = "composers_spotify.dat"


def enquire_name_match(target_name: str, result_name: str):
    """

    :param target_name: This is the name we searched for
    :param result_name: this is the name of one of the results
    :return: True if match, else False
    """
    read = input(f"Wir suchten nach: {target_name}, wir fanden: {result_name}")
    return read in ["", "y", "yes"]


#conn = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#with open(INPUT_FILE, "rb") as composer_list_pickled_file:
#    composer_list = pickle.load(composer_list_pickled_file)

def add_spotify_infos_to_composers(conn: Spotify, composers: List[Composer]) -> List[Composer]:
    for composer in composers:
        name_str = composer.name
        try:
            results = get_componist_search_results(conn, name_str)
        except TimeoutError:
            print(f"Timeout Error for {composer.name}")
        for result_uri, result_name in results.items():
            if unidecode_except_german_umlaute(result_name.lower()) \
                    == unidecode_except_german_umlaute(name_str.lower()):
                composer.spotify_id = result_uri
                props = get_composer_props(conn, composer.spotify_id,
                                           [ComposerProps.POPULARITY, ComposerProps.FOLLOWERS])
                composer.spotify_popularity = props[ComposerProps.POPULARITY]
                composer.spotify_followers = props[ComposerProps.FOLLOWERS]
                break

        if composer.spotify_id:
            continue

    return list(filter(lambda c: c.spotify_id, composers))



'''
    i = 0
    for result_uri, result_name in results.items():
        if enquire_name_match(name_str, result_name):
            composer.spotify_id = result_uri
            print(f"Used: {result_name} for {name_str}")
            break

        if i > 3:
            break
        i += 1

    if composer.spotify_id:
        continue

    uri = input(f"Input URI manually for {composer.name}:")
    if uri and uri != "n":
        composer.spotify_id = uri



composer_list_filtered = list(filter(lambda c: composer.spotify_id, composer_list))
composer_list_sorted_pop = sorted(composer_list_filtered, lambda c: get_composer_prop(ComposerProps.POPULARITY))
composer_list_sorted_fol = sorted(composer_list_filtered, lambda c: get_composer_prop(ComposerProps.FOLLOWERS))
print([c.name for c in composer_list_sorted_pop][:20])
print([c.name for c in composer_list_sorted_pop][:20])
'''