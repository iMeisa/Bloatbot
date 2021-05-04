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


def pp_calculation(map_id, mods=None, percentage=100.0, max_combo=None, miss_count=0) -> int:

    params = ''
    if mods is not None:
        params += ' +' + mods
    if percentage < 100:
        params += f' {percentage}%'
    if max_combo is not None:
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
    raw_acc = round((note_hit_count / note_total) * 100)
    beatmap_acc = raw_acc / 100

    return f'{beatmap_acc:.2f}%'


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


def pass_amount(rank, beatmap_only, beatmap_data, n0, n50, n100, n300) -> str:
    if rank == 'F' and not beatmap_only:
        circles = int(beatmap_data['count_normal'])
        sliders = int(beatmap_data['count_slider'])
        spinners = int(beatmap_data['count_spinner'])

        object_count = circles + sliders + spinners
        objects_hit = n0 + n50 + n100 + n300
        percentage = f'({str(int(objects_hit / object_count * 100))[:5]}% through)'

        return percentage
    return ''
