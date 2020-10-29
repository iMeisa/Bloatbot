import pickle
from ratelimit import limits, sleep_and_retry
from urllib.request import urlopen
from urllib.parse import urlencode
import json
from datetime import datetime
import os
import subprocess
import discord

# osu! API
with open('Cogs/Tools/osuAPI.pickle', 'rb') as fl:
    api_key = pickle.load(fl)


@sleep_and_retry
@limits(calls=60, period=60)
def call_api(url_param):
    url = 'https://osu.ppy.sh/api/' + url_param
    resp = urlopen(url)
    return json.load(resp)


def get_user_data(username):
    query = urlencode({'k': api_key, 'u': username})
    user_url = 'get_user' + '?' + query
    user_data = call_api(user_url)
    return user_data[0]


def get_beatmap_data(beatmap_id, mod_bytes_raw=0):
    current_mods = get_mods(mod_bytes_raw, separate=False)
    acceptable_mods = {'EZ': 2, 'HR': 16, 'DT': 64, 'HT': 256, 'NC': 64}

    change_sr = False
    used_mods = []
    for mod in acceptable_mods:
        if mod in current_mods:
            change_sr = True
            used_mods.append(mod)
            break

    mod_bytes = 0
    for mod in used_mods:
        mod_bytes += acceptable_mods[mod]

    if change_sr:
        mods = mod_bytes
    else:
        mods = 0

    query = urlencode({'k': api_key, 'b': beatmap_id, 'mods': mods})
    beatmap_url = 'get_beatmaps' + '?' + query
    beatmap_data = call_api(beatmap_url)
    return beatmap_data[0]


def get_mods(mod_id, separate=True):
    if mod_id is None or mod_id == '0':
        return 'None'
    mod_id = int(mod_id)

    mods = ['NF', 'EZ', 'Touch', 'HD', 'HR', 'SD', 'DT', 'RX', 'HT', 'NC', 'FL', 'AU', 'SO', 'AP', 'PF',
            'K4', 'K5', 'K6', 'K7', 'K8', 'FI', 'RD', 'CN', 'TG', 'K9', 'KC', 'K1', 'K3', 'K2', 'V2', 'MR']
    mod_list = []
    for i in range((len(mods) - 1), 0, -1):
        mod_value = 2 ** i
        if mod_id >= mod_value:
            mod_id -= mod_value
            mod_list.append(mods[i])
    mod_list.reverse()

    used_mods = ''
    for i in range(len(mod_list)):
        if separate:
            if i == (len(mod_list) - 1):
                used_mods += mod_list[i]
            else:
                used_mods += mod_list[i] + ', '
        else:
            used_mods += mod_list[i]

    return used_mods


# Recalculation specific to TTT
def mod_recalculate(score, mods):
    score = int(score)

    if mods in ['None', '']:
        score *= 0.72
        return int(score)

    multiplier = 1.0
    if 'EZ' in mods:
        multiplier += 0.75
    if 'SO' in mods:
        multiplier -= 0.2
    if 'FL' in mods:
        multiplier += 1.0

    return int(score * multiplier)


def get_time_diff(time_origin):
    fmt = '%Y-%m-%d %H:%M:%S'
    time_now = datetime.utcnow().strftime(fmt)
    time_diff = datetime.strptime(time_now, fmt) - datetime.strptime(time_origin, fmt)

    if time_diff.days < 1:
        if time_diff.seconds >= 3600:
            hours = time_diff.seconds // 3600
            if hours > 1:
                return f'{hours} hours ago'
            else:
                return '1 hour ago'
        elif time_diff.seconds >= 60:
            minutes = time_diff.seconds // 60
            if minutes > 1:
                return f'{minutes} minutes ago'
            else:
                return '1 minute ago'
        else:
            if time_diff.seconds > 1:
                return f'{time_diff.seconds} seconds ago'
            else:
                return '1 second ago'
    else:
        if time_diff.days >= 365:
            years = time_diff.days // 365
            if time_diff.days > 1:
                return f'{years} years ago'
            else:
                return '1 year ago'
        elif time_diff.days >= 30:
            months = time_diff.days // 30
            if months > 1:
                return f'{months} months ago'
            else:
                return '1 month ago'
        else:
            if time_diff.days > 1:
                return f'{time_diff.days} days ago'
            else:
                return '1 day ago'


def get_acc(n0, n50, n100, n300):
    note_hit_count = (50 * n50) + (100 * n100) + (300 * n300)
    note_total = 300 * (n0 + n50 + n100 + n300)
    raw_acc = round((note_hit_count / note_total) * 10000)
    beatmap_acc = str(raw_acc / 100)

    return beatmap_acc[:5]


def sec_to_min(seconds_raw):
    seconds = int(seconds_raw)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return f'{minutes}:{seconds}'


def pp_calculation(map_id, mods=None, percentage=100.0, max_combo=None, miss_count=0):
    if not os.path.isfile(f'./Cogs/Tools/oppai-cache/{map_id}.osu'):
        os.system(f'curl https://osu.ppy.sh/osu/{map_id} > ./Cogs/Tools/oppai-cache/{map_id}.osu')

    params = ''
    if mods is not None:
        params += ' +' + mods
    if percentage < 100:
        params += f' {percentage}%'
    if max_combo is not None:
        params += f' {max_combo}x'
    if miss_count > 0:
        params += f' {miss_count}m'

    pp_data = subprocess.check_output(f'oppai ./Cogs/Tools/oppai-cache/{map_id}.osu {params}',
                                      shell=True).decode('UTF-8').split('\n')
    map_pp_data = pp_data[-3].split()
    pp_total = round(float(map_pp_data[0]))
    return pp_total


def remove_param(user_string, param):
    param_len = len(param) + 1
    if user_string.endswith(param):
        return user_string[:-param_len]
    return user_string[param_len:]


def create_play_embed(user, beatmap_id=None, channel_id=None, beatmap_only=False, show_all=False):
    play_only = (beatmap_only + show_all) < 1  # True or False

    user_data = get_user_data(user)
    user_pfp = 'https://a.ppy.sh/' + user_data['user_id']

    # Create URL string
    if beatmap_id is None:
        # *r
        query = urlencode({'k': api_key, 'u': user, 'type': 'string', 'limit': 1})
        url = 'get_user_recent' + '?' + query
    else:
        # *c
        query = urlencode({'k': api_key, 'b': beatmap_id, 'u': user, 'm': 0, 'type': 'string', 'limit': 1})
        url = 'get_scores' + '?' + query

    # User data
    user_play_data = call_api(url)
    user_url = 'https://osu.ppy.sh/u/' + user
    username = user_data['username']
    user_pp = float(user_data['pp_raw'])
    user_global = int(user_data['pp_rank'])
    user_country = user_data['country']
    user_country_pp = int(user_data['pp_country_rank'])
    user_title = f'{username}: {user_pp:,}pp (#{user_global:,} {user_country}{user_country_pp})'

    # If received None
    if len(user_play_data) < 1:
        if channel_id is not None:
            return f"{user} hasn't clicked circles in a while"
        return f"{user} hasn't passed this map yet"

    # Assign beatmap data variable constants
    beatmap = user_play_data[0]
    if beatmap_id is None:
        beatmap_id = beatmap['beatmap_id']
    beatmap_data = get_beatmap_data(beatmap_id, beatmap['enabled_mods'])
    beatmap_cover = 'https://assets.ppy.sh/beatmaps/' + beatmap_data['beatmapset_id'] + '/covers/cover.jpg'
    beatmap_title = f'{beatmap_data["artist"]} - {beatmap_data["title"]} [{beatmap_data["version"]}]'
    beatmap_link = 'https://osu.ppy.sh/b/' + beatmap_id
    beatmap_score = int(beatmap['score'])
    beatmap_sr = float(beatmap_data['difficultyrating'][:4])

    # Mods
    enabled_mods = get_mods(beatmap['enabled_mods'])

    # Write data to file for *c
    if channel_id is not None:
        with open('./Cogs/Tools/recentbeatmaps.json', 'r') as f:
            recent_beatmaps = json.load(f)

        recent_beatmaps[str(channel_id)] = beatmap['beatmap_id']
        with open('./Cogs/Tools/recentbeatmaps.json', 'w') as f:
            json.dump(recent_beatmaps, f)

    # Determine rank status
    beatmap_rank_status = beatmap_data['approved']
    approve_status = 'last_updated'
    if beatmap_rank_status == '4':
        approve_status = 'loved'
        rank_status = ':heart:'
    elif beatmap_rank_status in ['3', '2']:
        approve_status = 'qualified'
        rank_status = ':white_check_mark:'
    elif beatmap_rank_status == '1':
        approve_status = 'ranked'
        rank_status = ':arrow_double_up:'
    elif beatmap_rank_status == '0':
        rank_status = ':clock3:'
    elif beatmap_rank_status == '-1':
        rank_status = ':tools:'
    else:
        rank_status = ':pirate_flag:'

    # Beatmap details
    beatmap_time = f'{sec_to_min(beatmap_data["total_length"])} ({sec_to_min(beatmap_data["hit_length"])})'
    beatmap_bpm = float(beatmap_data['bpm'])
    beatmap_max_combo = beatmap_data['max_combo']
    beatmap_cs = float(beatmap_data['diff_size'])
    beatmap_ar = float(beatmap_data['diff_approach'])
    beatmap_od = float(beatmap_data['diff_overall'])
    beatmap_hp = float(beatmap_data['diff_drain'])

    # Mapper details
    beatmap_mapper = beatmap_data['creator']
    mapper_id = beatmap_data['creator_id']
    if beatmap_data['approved_date'] is not None:
        upload_date = beatmap_data['approved_date']
    else:
        upload_date = beatmap_data['last_update']
    upload_time_diff = get_time_diff(upload_date)

    mapper_details = f'Mapped by {beatmap_mapper}, {approve_status} {upload_time_diff}'
    mapper_pfp = 'https://a.ppy.sh/' + mapper_id

    # Mod difficulty recalculation
    if 'HR' in enabled_mods:
        beatmap_cs *= 1.3
        beatmap_cs = round(beatmap_cs, 2)

        beatmap_ar *= 1.4
        beatmap_ar = round(beatmap_ar, 2)
        if beatmap_ar > 10:
            beatmap_ar = 10

        beatmap_od *= 1.4
        beatmap_od = round(beatmap_od, 2)
        if beatmap_od > 10:
            beatmap_od = 10

        beatmap_hp *= 1.4
        beatmap_hp = round(beatmap_hp, 2)
        if beatmap_hp > 10:
            beatmap_hp = 10

    elif 'EZ' in enabled_mods:
        beatmap_cs /= 2
        beatmap_ar /= 2
        beatmap_od /= 2
        beatmap_hp /= 2
    if 'DT' in enabled_mods:
        beatmap_ar = str(beatmap_ar) + '+'
        beatmap_od = str(beatmap_od) + '+'
        beatmap_hp = str(beatmap_hp) + '+'

        # BPM and Time recalculation
        beatmap_bpm = beatmap_bpm * 1.5

        time_total = sec_to_min(float(beatmap_data['total_length']) * 0.6666)
        time_drain = sec_to_min(float(beatmap_data['hit_length']) * 0.6666)
        beatmap_time = f'{time_total} ({time_drain})'

    elif 'HT' in enabled_mods:
        beatmap_ar = str(beatmap_ar) + '-'
        beatmap_od = str(beatmap_od) + '-'
        beatmap_hp = str(beatmap_hp) + '-'

        # BPM and Time recalculation
        beatmap_bpm = beatmap_bpm * 0.6666

        time_total = sec_to_min(float(beatmap_data['total_length']) * 1.5)
        time_drain = sec_to_min(float(beatmap_data['hit_length']) * 1.5)
        beatmap_time = f'{time_total} ({time_drain})'

    beatmap_difficulty = f'CS: `{beatmap_cs}` AR: `{beatmap_ar}`\n' \
                         f'OD: `{beatmap_od}` HP: `{beatmap_hp}`'
    beatmap_info = f'''Length: `{beatmap_time}`
                   BPM: `{int(beatmap_bpm)}`
                   Combo: `{beatmap_max_combo}`'''

    # Determine acc
    n0 = int(beatmap['countmiss'])
    n50 = int(beatmap['count50'])
    n100 = int(beatmap['count100'])
    n300 = int(beatmap['count300'])
    beatmap_acc = get_acc(n0, n50, n100, n300)
    score_title = f'{beatmap_score:,}  ({beatmap_acc[:5]}%)'

    # Combo count and notes
    score_combo = f'**{beatmap["maxcombo"]}x**/{beatmap_data["max_combo"]}X' \
                  f'\n{{ {n300} / {n100} / {n50} / {n0} }}'

    # Footer time diff
    time_diff = get_time_diff(beatmap['date'])

    # Calculate PP
    compressed_mods = get_mods(beatmap['enabled_mods'], separate=False)
    pp_achieved = pp_calculation(beatmap_id, mods=compressed_mods, percentage=float(beatmap_acc),
                                 max_combo=beatmap['maxcombo'], miss_count=n0)
    pp_max = pp_calculation(beatmap_id, mods=compressed_mods)

    if beatmap['rank'] == 'F':
        pp_value = f'~~**{pp_achieved}pp**/{pp_max}PP~~'
    elif beatmap_rank_status in ['2', '1']:
        pp_value = f'**{pp_achieved}pp**/{pp_max}PP'
    else:
        pp_value = f'~~**{pp_achieved}pp**/{pp_max}PP~~'

    # Theoretical pp values
    pp_95 = pp_calculation(beatmap_id, mods=compressed_mods, percentage=95)
    pp_98 = pp_calculation(beatmap_id, mods=compressed_mods, percentage=98)
    pp_99 = pp_calculation(beatmap_id, mods=compressed_mods, percentage=99)

    theoretical_pp = f'95%: `{pp_95}pp`\n98%: `{pp_98}pp`\n99%: `{pp_99}pp`\n100%: `{pp_max}pp`'

    # Calculate map progress if failed
    pass_percentage = ''
    if beatmap['rank'] == 'F' and not beatmap_only:
        circles = int(beatmap_data['count_normal'])
        sliders = int(beatmap_data['count_slider'])
        spinners = int(beatmap_data['count_spinner'])

        object_count = circles + sliders + spinners
        objects_hit = n0 + n50 + n100 + n300
        pass_percentage = f'({str(int(objects_hit / object_count * 100))[:5]}% through)'

    # Create embed
    embed = discord.Embed(
        title=rank_status + ' ' + beatmap_title,
        url=beatmap_link,
        description=f'**{beatmap_sr}** :star: {pass_percentage}',
        image=beatmap_cover
    )

    # Set embed color based on rank
    if beatmap_only:
        embed.colour = discord.Color.teal()
    elif beatmap['rank'] in ['SH', 'SSH']:
        embed.colour = discord.Color.light_grey()
    elif beatmap['rank'] in ['S', 'SS']:
        embed.colour = discord.Color.gold()
    elif beatmap['rank'] == 'A':
        embed.colour = discord.Color.dark_green()
    elif beatmap['rank'] == 'B':
        embed.colour = discord.Color.blue()
    elif beatmap['rank'] == 'C':
        embed.colour = discord.Color.purple()
    elif beatmap['rank'] == 'D':
        embed.colour = discord.Color.red()

    embed.set_author(name=user_title, icon_url=user_pfp, url=user_url)
    embed.set_image(url=beatmap_cover)

    if play_only or show_all:
        embed.add_field(name=score_title, value=score_combo, inline=True)
        embed.add_field(name='Mods:', value=enabled_mods, inline=True)
        embed.add_field(name='PP:', value=pp_value, inline=True)
        embed.set_footer(text=time_diff)
    if beatmap_only or show_all:
        if show_all:
            embed.add_field(name='-' * 80, value=f'**{"-" * 80}**', inline=False)
        embed.add_field(name='Beatmap Difficulty', value=beatmap_difficulty, inline=True)
        embed.add_field(name='Beatmap Info', value=beatmap_info, inline=True)
        embed.add_field(name='PP Values:', value=theoretical_pp, inline=True)
        embed.set_footer(text=mapper_details, icon_url=mapper_pfp)

    praise = None
    if beatmap['rank'] in ['S', 'SH']:
        praise = 'Nice S'
    elif beatmap['rank'] in ['SS', 'SSH']:
        praise = 'Nice SS'

    return embed, praise
