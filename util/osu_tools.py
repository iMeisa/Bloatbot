import json
import os
import subprocess


def get_mods(mod_id: int, separate: bool = True) -> str:
    if mod_id is None or mod_id == '0':
        return 'None'

    mod_id = int(mod_id)

    mods = ['NF', 'EZ', 'Touch', 'HD', 'HR', 'SD', 'DT', 'RX', 'HT', 'NC', 'FL', 'AU', 'SO', 'AP', 'PF',
            'K4', 'K5', 'K6', 'K7', 'K8', 'FI', 'RD', 'CN', 'TG', 'K9', 'KC', 'K1', 'K3', 'K2', 'V2', 'MR']
    mod_list = []
    for i in range((len(mods) - 1), -1, -1):
        mod_value = 2 ** i
        if mod_id >= mod_value:
            mod_id -= mod_value
            mod_list.append(mods[i])
    mod_list.reverse()

    used_mods = str()
    for i in range(len(mod_list)):
        if separate:
            if i == (len(mod_list) - 1):
                used_mods += mod_list[i]
            else:
                used_mods += mod_list[i] + ', '
        else:
            used_mods += mod_list[i]

    return used_mods


def oppai(map_id, *, params) -> list:
    if not os.path.isfile(f'oppai_cache/{map_id}.osu'):
        os.system(f'curl https://osu.ppy.sh/osu/{map_id} > oppai_cache/{map_id}.osu')

    oppai_data = subprocess.check_output(f'oppai oppai_cache/{map_id}.osu {params}', shell=True)\
        .decode('UTF-8').split('\n')

    return oppai_data


def pp_calculation(map_id, mods: str = None, percentage: float = 100.0, max_combo: int = 0, miss_count: int = 0) -> int:
    mods = mods if mods is not None else 'None'

    params = ''
    if mods != 'None':
        params += ' +' + mods
    if percentage < 100:
        params += f' {percentage}%'
    if max_combo > 0:
        params += f' {max_combo}x'
    if miss_count > 0:
        params += f' {miss_count}m'

    oppai_data = oppai(map_id=map_id, params=params)
    map_pp_data = oppai_data[-3].split()
    pp_total = round(float(map_pp_data[0]))
    return pp_total


def get_acc(n0: int, n50: int, n100: int, n300: int) -> str:
    note_hit_count = (50 * n50) + (100 * n100) + (300 * n300)
    note_total = 300 * (n0 + n50 + n100 + n300)
    raw_acc = (note_hit_count / note_total) * 100

    return f'{raw_acc:.2f}%'


def rank_emoji(rank_status: int) -> (str, str):
    approve_status = 'last_updated'
    if rank_status == 4:
        approve_status = 'loved'
        rank_status = ':heart:'
    elif rank_status in [3, 2]:
        approve_status = 'qualified'
        rank_status = ':white_check_mark:'
    elif rank_status == 1:
        approve_status = 'ranked'
        rank_status = ':arrow_double_up:'
    elif rank_status == 0:
        rank_status = ':clock3:'
    elif rank_status == -1:
        rank_status = ':tools:'
    else:
        rank_status = ':pirate_flag:'

    return rank_status, approve_status


# def pass_amount(rank, beatmap_only, beatmap_data, n0, n50, n100, n300) -> str:
#     if rank == 'F' and not beatmap_only:
#         circles = int(beatmap_data['count_normal'])
#         sliders = int(beatmap_data['count_slider'])
#         spinners = int(beatmap_data['count_spinner'])
#
#         object_count = circles + sliders + spinners
#         objects_hit = n0 + n50 + n100 + n300
#         percentage = f'({str(int(objects_hit / object_count * 100))[:5]}% through)'
#
#         return percentage
#     return ''


def get_api_mods(mod_bytes_raw) -> int:
    current_mods = get_mods(mod_bytes_raw, separate=False)
    acceptable_mods = {'EZ': 2, 'HR': 16, 'DT': 64, 'HT': 256, 'NC': 64}

    mods = 0

    for mod in acceptable_mods:
        if mod in current_mods:
            mods += acceptable_mods[mod]

    return mods


def get_registered_user(discord_id):
    discord_id = str(discord_id)
    with open('cache/users.json', 'r') as f:
        users = json.load(f)

    if discord_id not in list(users.keys()):
        return None

    return users[discord_id]


def get_recent_beatmap(channel_id: str) -> str:
    with open('cache/recentbeatmaps.json', 'r') as f:
        recent_beatmaps = json.load(f)

    return recent_beatmaps[str(channel_id)]


def add_recent_beatmap(channel_id: str, beatmap_id: str):
    with open('cache/recentbeatmaps.json', 'r') as f:
        recent_beatmaps = json.load(f)

    recent_beatmaps[str(channel_id)] = beatmap_id

    with open('cache/recentbeatmaps.json', 'w') as f:
        json.dump(recent_beatmaps, f)
