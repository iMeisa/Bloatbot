import json
import pickle
from urllib.parse import urlencode
from urllib.request import urlopen

from classes.beatmap import Beatmap
from util.osu_tools import get_acc, get_mods, get_api_mods, pp_calculation
from util.time_format import get_time_diff


class Score:
    def __init__(self, play_data: dict):
        self.beatmap_id = play_data['beatmap_id']
        self.score = int(play_data['score'])
        self.max_combo = int(play_data['maxcombo'])
        self.count50 = int(play_data['count50'])
        self.count100 = int(play_data['count100'])
        self.count300 = int(play_data['count300'])
        self.count_miss = int(play_data['countmiss'])
        self.acc = get_acc(self.count_miss, self.count50, self.count100, self.count300)
        self.count_katu = int(play_data['countkatu'])
        self.count_geki = int(play_data['countgeki'])
        self.perfect = play_data['perfect'] == '1'
        self.enabled_mods_bytes = play_data['enabled_mods']
        self.enabled_mods = get_mods(self.enabled_mods_bytes, separate=False)
        self.user_id = play_data['user_id']
        self.date = play_data['date']
        self.when_played = get_time_diff(self.date)
        self.rank = play_data['rank']
        self.pp = pp_calculation(self.beatmap_id, mods=self.enabled_mods,
                                 percentage=float(self.acc[:-1]), max_combo=self.max_combo, miss_count=self.count_miss)
        self.beatmap = _get_beatmap_(self.beatmap_id, self.enabled_mods_bytes)
        self.pass_amount = _pass_amount_(self.beatmap.circle_count, self.beatmap.slider_count,
                                         self.beatmap.spinner_count, self.count_miss, self.count50,
                                         self.count100, self.count300)


def _get_beatmap_(beatmap_id, mod_bytes_raw=0) -> Beatmap:
    mods = get_api_mods(mod_bytes_raw)

    with open('keys/osuAPI.pickle', 'rb') as fl:
        api_key = pickle.load(fl)
    query = urlencode({'k': api_key, 'b': beatmap_id, 'mods': mods})
    beatmap_url = 'https://osu.ppy.sh/api/get_beatmaps?' + query
    resp = urlopen(beatmap_url)
    beatmap_json = json.load(resp)

    return Beatmap(beatmap_json[0])


def _pass_amount_(circles, sliders, spinners, n0, n50, n100, n300) -> str:
    object_count = circles + sliders + spinners
    objects_hit = n0 + n50 + n100 + n300
    percentage = f'({int(objects_hit / object_count * 100)}% through)'

    return percentage
