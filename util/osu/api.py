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
    """
    Gives osu! user details

    :param username: osu! username or ID `string`
    :param is_id: If provided username is an ID `bool`
    :return: User class of osu! user `User`
    """

    name_type = 'string' if not is_id else 'id'
    query = urlencode({'k': API_KEY, 'u': username, 'type': name_type})
    user_url = 'get_user' + '?' + query
    user_data = call_api(user_url)[0]

    return User(user_data)


def get_beatmap(beatmap_id, mod_bytes_raw=0) -> Beatmap:
    """
    Gives beatmap details from beatmap ID

    :param beatmap_id: Beatmap ID
    :param mod_bytes_raw:
    :return:
    """

    mods = get_api_mods(mod_bytes_raw)

    query = urlencode({'k': API_KEY, 'b': beatmap_id, 'mods': mods})
    beatmap_url = 'get_beatmaps' + '?' + query
    print('beatmap_url:', beatmap_url)
    beatmap_data = call_api(beatmap_url)[0]

    return Beatmap(beatmap_data)


def get_recent_play(osu_id):
    """
    Gives the most recent play of a user in the last 24 hours

    Returns None if no plays in the last 24 hours

    :param osu_id: osu! ID `string` or `int`
    :return: Score class of the most recent play `Score`
    """

    query = urlencode({'k': API_KEY, 'u': osu_id, 'type': 'id', 'limit': 1})
    url = 'get_user_recent' + '?' + query
    scores = call_api(url)

    if len(scores) < 1:
        return None

    return Score(scores[0])


def get_user_map_best(beatmap_id, user_id):
    """
    Gives best play of user on given beatmap

    Returns None if user has no plays on given beatmap

    :param beatmap_id: Beatmap ID `string` or `int`
    :param user_id: osu! ID `string` or `int`
    :return: Score class of best play `Score`
    """

    query = urlencode({'k': API_KEY, 'b': beatmap_id, 'u': user_id})
    url = 'get_scores' + '?' + query
    scores = call_api(url)

    if len(scores) < 1:
        return None

    return Score(scores[0], beatmap_id=beatmap_id)
