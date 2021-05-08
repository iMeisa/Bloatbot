import pickle
from ratelimit import limits, sleep_and_retry
from urllib.request import urlopen
from urllib.parse import urlencode
import json

from classes.beatmap import Beatmap
from classes.score import Score
from classes.user import User

# osu! API key
from util.osu.tools import get_api_mods

with open('keys/osuAPI.pickle', 'rb') as fl:
    API_KEY = pickle.load(fl)


@sleep_and_retry
@limits(calls=60, period=60)
def call_api(url_param) -> dict:
    url = 'https://osu.ppy.sh/api/' + url_param
    resp = urlopen(url)
    return json.load(resp)


def get_user(username, is_id=False) -> User:
    name_type = 'string' if not is_id else 'id'
    query = urlencode({'k': API_KEY, 'u': username, 'type': name_type})
    user_url = 'get_user' + '?' + query
    user_data = call_api(user_url)[0]

    return User(user_data)


def get_beatmap(beatmap_id, mod_bytes_raw=0) -> Beatmap:
    mods = get_api_mods(mod_bytes_raw)

    query = urlencode({'k': API_KEY, 'b': beatmap_id, 'mods': mods})
    beatmap_url = 'get_beatmaps' + '?' + query
    print('beatmap_url:', beatmap_url)
    beatmap_data = call_api(beatmap_url)[0]

    return Beatmap(beatmap_data)


def get_recent_play(osu_id):
    query = urlencode({'k': API_KEY, 'u': osu_id, 'type': 'id', 'limit': 1})
    url = 'get_user_recent' + '?' + query
    scores = call_api(url)

    if len(scores) < 1:
        return None

    return Score(scores[0])


def get_user_map_best(beatmap_id, user_id):
    query = urlencode({'k': API_KEY, 'b': beatmap_id, 'u': user_id})
    url = 'get_scores' + '?' + query
    scores = call_api(url)

    if len(scores) < 1:
        return None

    return Score(scores[0], beatmap_id=beatmap_id)
