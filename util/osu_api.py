import pickle
from ratelimit import limits, sleep_and_retry
from urllib.request import urlopen
from urllib.parse import urlencode
import json

from classes.beatmap import Beatmap
from classes.user import User

# osu! API key
from util.osu_tools import get_mods

with open('keys/osuAPI.pickle', 'rb') as fl:
    API_KEY = pickle.load(fl)


@sleep_and_retry
@limits(calls=60, period=60)
def call_api(url_param) -> dict:
    url = 'https://osu.ppy.sh/api/' + url_param
    resp = urlopen(url)
    return json.load(resp)


def get_user_data(username) -> User:
    query = urlencode({'k': API_KEY, 'u': username})
    user_url = 'get_user' + '?' + query
    user_data = call_api(user_url)[0]

    return User(user_data)


def get_beatmap(beatmap_id, mod_bytes_raw=0) -> Beatmap:
    current_mods = get_mods(mod_bytes_raw, separate=False)
    acceptable_mods = {'EZ': 2, 'HR': 16, 'DT': 64, 'HT': 256, 'NC': 64}

    mods = 0

    for mod in acceptable_mods:
        if mod in current_mods:
            mods += acceptable_mods[mod]

    query = urlencode({'k': API_KEY, 'b': beatmap_id, 'mods': mods})
    beatmap_url = 'get_beatmaps' + '?' + query
    beatmap_data = call_api(beatmap_url)[0]

    return Beatmap(beatmap_data)



