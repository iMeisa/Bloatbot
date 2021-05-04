from util.osu_api import get_beatmap
from util.osu_tools import get_acc, get_mods


class Play:

    def __init__(self, play_data: dict):
        self.beatmap = get_beatmap(play_data['beatmap_id'])
        self.score = play_data['score']
        self.max_combo = play_data['maxcombo']
        self.count50 = int(play_data['count50'])
        self.count100 = int(play_data['count100'])
        self.count300 = int(play_data['count300'])
        self.count_miss = int(play_data['countmiss'])
        self.acc = get_acc(self.count_miss, self.count50, self.count100, self.count300)
        self.count_katu = play_data['countkatu']
        self.count_geki = play_data['countgeki']
        self.perfect = play_data['perfect'] == '1'
        self.enabled_mods_bytes = play_data['enabled_mods']
        self.enabled_mods = get_mods(self.enabled_mods_bytes)
        self.user_id = play_data['user_id']
        self.date = play_data['date']
        self.rank = play_data['rank']
