import json
import os
import subprocess

mod_name_list = ['NF', 'EZ', 'TD', 'HD', 'HR', 'SD', 'DT', 'RX', 'HT', 'NC', 'FL', 'AU', 'SO', 'AP', 'PF',
                 'K4', 'K5', 'K6', 'K7', 'K8', 'FI', 'RD', 'CN', 'TG', 'K9', 'KC', 'K1', 'K3', 'K2', 'V2', 'MR']


def get_mods(mod_id: int, separate: bool = True) -> str:
    """
    Returns a string of mods from the bitwise mod value

    :param mod_id: Bitwise mod value
    :param separate: Return string separated by commas or as one word
    :return: String of mods
    """

    if mod_id is None or mod_id == '0':
        return 'None'

    # Get mod bits
    mod_id = int(mod_id)
    mod_list = []
    for i in range((len(mod_name_list) - 1), -1, -1):
        mod_value = 1 << i
        if mod_id >= mod_value:
            mod_id -= mod_value
            mod_list.append(mod_name_list[i])
    mod_list.reverse()

    # Remove redundant mods
    if 'NC' in mod_list:
        mod_list.remove('DT')
    if 'PF' in mod_list:
        mod_list.remove('SD')

    # Format string
    used_mods = ''.join(mod_list) if not separate else ', '.join(mod_list)

    return used_mods


def get_mods_id(enabled_mods: str) -> int:
    """
    Converts a non-separated string of mods into a bitwise value

    :param enabled_mods: Non-separated string of mods
    :return: Bitwise mod value `int`
    """

    if enabled_mods is None:
        return 0

    mod_bytes = 0
    for i in range(0, len(enabled_mods), 2):
        mod = enabled_mods[i:i+2].upper()
        if mod not in mod_name_list:
            continue

        mod_index = mod_name_list.index(mod)
        mod_value = 1 << mod_index

        # Add redundant mods
        if mod_value == 512:  # Add DT to NC
            mod_value += 64
        if mod_value == 16384:  # Add SD to PF
            mod_value += 32

        mod_bytes += mod_value

    return mod_bytes


def oppai(map_id, oppai_params) -> list:
    """
    Returns beatmap data from the oppai tool

    :param map_id: Beatmap ID
    :param oppai_params: Oppai params, i.e. (+HDDT)
    :return: Oppai output lines as `list`
    """

    if not os.path.isfile(f'oppai_cache/{map_id}.osu'):
        os.system(f'curl https://osu.ppy.sh/osu/{map_id} > oppai_cache/{map_id}.osu')

    oppai_data = subprocess.check_output(f'oppai oppai_cache/{map_id}.osu {oppai_params}', shell=True)\
        .decode('UTF-8').split('\n')

    return oppai_data


def pp_calculation(map_id, mods: str = None, percentage: float = 100.0, max_combo: int = 0, miss_count: int = 0) -> int:
    """
    Calculates PP from the oppai tool

    :param map_id: Beatmap ID
    :param mods: Non-separated `string` of mods
    :param percentage: Play acc `float`
    :param max_combo: Play max combo `int`
    :param miss_count: Play miss count `int`
    :return: PP of given play `int`
    """

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

    oppai_data = oppai(map_id=map_id, oppai_params=params)
    map_pp_data = oppai_data[-3].split()
    pp_total = round(float(map_pp_data[0]))
    return pp_total


def get_acc(n0: int, n50: int, n100: int, n300: int) -> str:
    """
    Gives acc based on all 300s, 100s, 50s and misses

    :param n0: Miss count
    :param n50: 50 count
    :param n100: 100 count
    :param n300: 300 count
    :return: Acc `string` to 2 decimal points
    """

    note_hit_count = (50 * n50) + (100 * n100) + (300 * n300)
    note_total = 300 * (n0 + n50 + n100 + n300)
    raw_acc = (note_hit_count / note_total) * 100

    return f'{raw_acc:.2f}%'


def rank_emoji(rank_status: int) -> (str, str):
    """
    Gives emoji based on beatmap rank status and rank term
    :param rank_status: Rank status value `int`
    :return: (emoji `string`, rank term `string`)
    """

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


def get_api_mods(mod_bytes_raw) -> int:
    """
    Gives bitwise mod value accepted by api

    :param mod_bytes_raw: Bitwise mod value `int`
    :return: Bitwise mod value the api cares about `int`
    """

    current_mods = get_mods(mod_bytes_raw, separate=False)
    acceptable_mods = {'EZ': 2, 'HR': 16, 'DT': 64, 'HT': 256, 'NC': 64}

    mods = 0

    for mod in acceptable_mods:
        if mod in current_mods:
            mods += acceptable_mods[mod]

    return mods


def get_registered_user(discord_id):
    """
    Gives osu id of registered discord user

    Returns None if not registered

    :param discord_id: Discord ID of user `string`
    :return: osu ID of user `string`
    """

    discord_id = str(discord_id)
    with open('cache/users.json', 'r') as f:
        users = json.load(f)

    if discord_id not in list(users.keys()):
        return None

    return users[discord_id]


def get_recent_beatmap(channel_id: str) -> str:
    """
    Gives beatmap ID most recently shown in given channel

    :param channel_id: Channel ID `string`
    :return: Beatmap ID `string`
    """

    with open('cache/recentbeatmaps.json', 'r') as f:
        recent_beatmaps = json.load(f)

    return recent_beatmaps[str(channel_id)]


def add_recent_beatmap(channel_id: str, beatmap_id: str):
    """
    Update most recently shown beatmap in given channel

    :param channel_id: Channel ID `string`
    :param beatmap_id: Beatmap ID `string`
    """

    with open('cache/recentbeatmaps.json', 'r') as f:
        recent_beatmaps = json.load(f)

    recent_beatmaps[str(channel_id)] = beatmap_id

    with open('cache/recentbeatmaps.json', 'w') as f:
        json.dump(recent_beatmaps, f)
