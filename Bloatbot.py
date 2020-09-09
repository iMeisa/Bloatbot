import discord
from discord.ext import commands
from random import randint
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import pickle
from ratelimit import limits, sleep_and_retry
from datetime import datetime

with open('token.txt', 'r') as fl:
    TOKEN = fl.read()
client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    watermelon = randint(1, 100) == 50
    if watermelon:
        await message.channel.send(':watermelon:')

    if message.content.lower() in ['hi', 'hello', 'o/']:
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('o/')
    if 'bloatbot' in message.content.lower():
        if message.author.display_name != 'Bloatbot':
            await message.channel.send(':blowfish:')
    if 'good bot' in message.content.lower():
        await message.channel.send(':D')
    if 'bad bot' in message.content.lower():
        await message.channel.send('D:')

    if message.content.lower() == 'bot':
        await message.channel.send(':eyes:')
    if 'better' in message.content:
        await message.channel.send(':clap:')
    if message.content.lower().startswith('oof'):
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('Oof')
    if message.content.lower() == 'nice' or '69' in message.content:
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('Nice')
    if message.content == '!r':
        await message.channel.send("You didn't use my *r command :(")
    elif 'boatbot' in message.content.lower() or message.author.display_name == 'OsuBot':
        await message.channel.send(':sailboat:')
    if message.content.lower() == 'f' and message.author.display_name != 'Bloatbot':
        await message.channel.send('F')
    if message.content.lower().endswith('pp') or 'pp ' in message.content.lower():
        await message.channel.send('filthy farmer')
    if ' tb ' in message.content.lower() or message.content.lower().startswith('tb hype'):
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('TB HYPE')
    if 'good song' in message.content.lower():
        await message.channel.send(':notes:')
    if 'good enough' in message.content.lower():
        await message.channel.send(':thumbup:')
    if 'streams' in message.content.lower():
        await message.channel.send('zxzxzxzxzx')
    if 'jumps' in message.content.lower():
        await message.channel.send('1 2 1 2 1 2')
    if ' won ' in message.content.lower() or message.content.lower().endswith(' won'):
        await message.channel.send(':first_place:')
    if 'yay' in message.content.lower():
        await message.channel.send('\\o/')
    if message.content.lower().startswith('hm'):
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('Hmmm')
    if message.content.lower().endswith('beast'):
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('BEAST')
    if message.author.display_name == 'Aupsie' or message.content.lower() == 'oi':
        if message.author.display_name != 'Bloatbot':
            aupsie = randint(1, 1000) == 500
            if aupsie:
                await message.channel.send('oi')

    await client.process_commands(message)


@client.command()
async def ask(ctx, *, question='blank'):
    responses = ['It is certain',
                 'It is decidedly so',
                 'Without a doubt',
                 'Yes definitely',
                 'You may rely on it',
                 'As I see it, yes',
                 'Most likely',
                 'Outlook good',
                 'yes',
                 'Signs point to yes',
                 'Reply hazy try again',
                 'Ask again later',
                 'Better not tell you now',
                 'Cannot predict now',
                 'Concentrate and ask again',
                 'Do not count on it',
                 'My reply is no',
                 'My sources say no',
                 'Outlook not so good',
                 'Very doubtful']

    if question == 'blank':
        await ctx.send('Please ask a question')
    else:
        number = randint(0, len(responses) - 1)
        await ctx.send(responses[number])


@client.command()
async def ping(ctx):
    await ctx.send(f'Pinged for {round(client.latency * 1000)}ms')


@client.command()
async def hi(ctx):
    author = str(ctx.author)
    await ctx.send(f'o/ {author[: -5]}')


@client.command()
async def say(ctx, *, statement):
    await ctx.channel.purge(limit=1)
    await ctx.send(statement)


@client.command()
async def loop(ctx, *, statement):
    for i in range(5):
        await ctx.send(statement)


@client.command()
async def version(ctx):
    with open('version.txt', 'r') as f:
        await ctx.send(f.read())


@client.command()
async def poke(ctx):
    if ctx.author.display_name != 'Bloatbot':
        await ctx.send('*poke')


@client.command()
async def roll(ctx, *, arg='string'):
    exists_arg = False
    if arg == 'string':
        maximum = 100
    elif not arg.isdigit():
        maximum = 100
        exists_arg = True
    else:
        maximum = int(arg)
    max_range = int(maximum)
    number = randint(1, max_range + 1)
    if exists_arg:
        await ctx.send(f'{arg}: {number}')
    else:
        await ctx.send(f'{number} points')


@client.command()
async def choose(ctx, *, arg='invalid'):
    choices = str.split(arg)
    choice1 = ''
    choice2 = ''
    if 'or' in choices:
        choice1_end = choices.index('or')
        for i in range(choice1_end):
            choice1 += choices[i] + ' '
        for i in range(choice1_end + 1, len(choices)):
            choice2 += choices[i] + ' '

        random_choice = randint(1, 2)
        if random_choice == 1:
            await ctx.send(choice1)
        else:
            await ctx.send(choice2)
    else:
        await ctx.send('Proper format: *choose (choice 1) or (choice 2)')


@client.command()
async def poll(ctx, *, params):
    poll_letters = '🇦🇧🇨🇩'
    single_quotes = "'" in params
    if single_quotes:
        options = params.split("'")
    else:
        options = params.split('"')

    for option in options:
        if option == ' ':
            options.remove(option)

    options.pop(0)
    question = options[0]
    options.pop(0)
    option_count = len(options)

    for i in range(option_count - 1):
        if i == len(poll_letters):
            break
        question += f'\n{poll_letters[i]} {options[i]}'

    msg = await ctx.send(question)
    for i in range(option_count - 1):
        await msg.add_reaction(poll_letters[i])


# osu! API
with open('osuAPI.pickle', 'rb') as fl:
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


def get_beatmap_data(beatmap_id):
    query = urlencode({'k': api_key, 'b': beatmap_id})
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
    for i in range((len(mods) - 1), 1, -1):
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


def mod_recalculate(score, mods):
    score = int(score)

    if mods in ['None', '']:
        score *= 0.72
        return str(int(score))

    multiplier = 1.0
    if 'EZ' in mods:
        multiplier += 0.75
    if 'SO' in mods:
        multiplier -= 0.2
    if 'FL' in mods:
        multiplier += 1.0

    return str(int(score * multiplier))


def get_time_diff(time_origin):
    fmt = '%Y-%m-%d %H:%M:%S'
    time_now = datetime.utcnow().strftime(fmt)
    time_diff = datetime.strptime(time_now, fmt) - datetime.strptime(time_origin, fmt)

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


def get_acc(n0, n50, n100, n300):
    note_hit_count = (50 * n50) + (100 * n100) + (300 * n300)
    note_total = 300 * (n0 + n50 + n100 + n300)
    raw_acc = round((note_hit_count / note_total) * 10000)
    beatmap_acc = str(raw_acc / 100)

    return beatmap_acc[:5]


def sec_to_min(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds - (minutes * 60)
    if seconds < 10:
        seconds = '0' + str(seconds)
    return f'{minutes}:{seconds}'


def remove_param(user_string, param):
    if user_string.endswith(param):
        return user_string[:-3]
    return user_string[3:]


@client.command()
async def r(ctx, *, user_param=''):

    beatmap_only = False
    show_all = False
    if '-a' in user_param:
        if '-b' in user_param:
            raise Exception('Used other params with -a')
        show_all = True
        user = remove_param(user_param, '-a')
    elif '-b' in user_param:
        beatmap_only = True
        user = remove_param(user_param, '-b')
    else:
        user = ctx.author.display_name

    play_only = (beatmap_only + show_all) < 1  # True or False

    user_data = get_user_data(user)
    user_pfp = 'https://a.ppy.sh/' + user_data['user_id']

    query = urlencode({'k': api_key, 'u': user, 'type': 'string', 'limit': 1})
    recent_url = 'get_user_recent' + '?' + query

    # User data
    user_recent = call_api(recent_url)
    user_url = 'https://osu.ppy.sh/u/' + user
    user_pp = float(user_data['pp_raw'])
    user_global = int(user_data['pp_rank'])
    user_country = user_data['country']
    user_country_pp = int(user_data['pp_country_rank'])
    user_title = f'{user}: {user_pp:,}pp (#{user_global:,} {user_country}{user_country_pp})'

    if len(user_recent) < 1:
        await ctx.send(f"{user} hasn't clicked circles in a while")
        raise FileNotFoundError

    beatmap = user_recent[0]
    beatmap_data = get_beatmap_data(beatmap['beatmap_id'])
    beatmap_cover = 'https://assets.ppy.sh/beatmaps/' + beatmap_data['beatmapset_id'] + '/covers/cover.jpg'
    beatmap_title = f'{beatmap_data["artist"]} - {beatmap_data["title"]} [{beatmap_data["version"]}]'
    beatmap_link = 'https://osu.ppy.sh/b/' + beatmap['beatmap_id']
    beatmap_score = int(beatmap['score'])
    beatmap_sr = beatmap_data['difficultyrating'][:4]

    # Determine rank status
    beatmap_rank_status = beatmap_data['approved']
    if beatmap_rank_status == '4':
        rank_status = ':heart:'
    elif beatmap_rank_status in ['3', '2']:
        rank_status = ':white_check_mark:'
    elif beatmap_rank_status == '1':
        rank_status = ':arrow_double_up:'
    elif beatmap_rank_status == '0':
        rank_status = ':clock3:'
    elif beatmap_rank_status == '-1':
        rank_status = ':tools:'
    else:
        rank_status = ':pirate_flag:'

    # Beatmap details
    beatmap_time = f'{sec_to_min(beatmap_data["total_length"])} ({sec_to_min(beatmap_data["hit_length"])})'
    beatmap_bpm = beatmap_data['bpm']
    beatmap_max_combo = beatmap_data['max_combo']
    beatmap_cs = beatmap_data['diff_size']
    beatmap_ar = beatmap_data['diff_approach']
    beatmap_od = beatmap_data['diff_overall']
    beatmap_hp = beatmap_data['diff_drain']

    beatmap_difficulty = f'CS: `{beatmap_cs}` AR: `{beatmap_ar}`\n' \
                         f'OD: `{beatmap_od}` HP: `{beatmap_hp}`'
    beatmap_info = f'Length: `{beatmap_time}`\n' \
                   f'BPM: `{beatmap_bpm}` Combo: `{beatmap_max_combo}`'

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

    # Mods
    enabled_mods = get_mods(beatmap['enabled_mods'])

    # Footer time diff
    time_diff = get_time_diff(beatmap['date'])

    # Create embed
    embed = discord.Embed(
        title=rank_status+' '+beatmap_title,
        url=beatmap_link,
        description=f'**{beatmap_sr}** :star:',
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
        embed.set_footer(text=time_diff)
    if beatmap_only or show_all:
        if show_all:
            embed.add_field(name='-' * 80, value=f'**{"-" * 80}**', inline=False)
        embed.add_field(name='Beatmap Difficulty', value=beatmap_difficulty, inline=True)
        embed.add_field(name='Beatmap Info', value=beatmap_info, inline=True)

    await ctx.send(embed=embed)


@client.command()
async def ttt(ctx, *, params=''):
    params = params.split()
    match_link = params[0]
    comments = ''
    if len(params) > 1:
        comment_words = params[1:]
        for word in comment_words:
            comments += word + ' '

    match_url_split = match_link.split('/')
    match_id = match_url_split[-1]
    query = urlencode({'k': api_key, 'mp': match_id})
    url_params = 'get_match?' + query
    match_data = call_api(url_params)

    match_title = match_data['match']['name']
    match_games = match_data['games']

    mappool = {}
    with open('tttmappool.txt', 'r') as f:
        mappool_raw = f.read().split('\n')
        for beatmap in mappool_raw:
            beatmap_pool_id = beatmap.split(' ')
            pool_id = beatmap_pool_id[1]
            map_id = beatmap_pool_id[0]
            mappool[map_id] = pool_id

    match_scores = []
    player_scores = {}
    user_ids = {}
    for game in match_games:
        game_scores = game['scores']

        beatmap_id = game['beatmap_id']
        if beatmap_id not in mappool:
            continue
        mappool_id = mappool[beatmap_id]

        score1 = game_scores[0]
        score2 = game_scores[1]
        user_id1 = score1['user_id']
        user_id2 = score2['user_id']

        player1_score = score1['score']
        player2_score = score2['score']
        free_mod = 'FM' in mappool_id or 'TB' in mappool_id
        if free_mod:
            player1_mods = get_mods(score1['enabled_mods'], separate=False)
            player2_mods = get_mods(score2['enabled_mods'], separate=False)
            player1_score = mod_recalculate(player1_score, player1_mods)
            player2_score = mod_recalculate(player2_score, player2_mods)

        if user_id1 not in player_scores:
            player_scores[user_id1] = 0
            player_scores[user_id2] = 0
            user_ids[user_id1] = get_user_data(user_id1)['username']
            user_ids[user_id2] = get_user_data(user_id2)['username']

        if player1_score > player2_score:
            player_scores[user_id1] += 1
        else:
            player_scores[user_id2] += 1

        beatmap_data = get_beatmap_data(beatmap_id)
        beatmap_title = f'{mappool_id}: _{beatmap_data["artist"]} - {beatmap_data["title"]}_'

        match_scores.append([beatmap_title, user_id1, player1_score, user_id2, player2_score])

    player1_id = list(user_ids.keys())[0]
    player2_id = list(user_ids.keys())[1]
    if player_scores[player1_id] > player_scores[player2_id]:
        final_score = f'**{user_ids[player1_id]} {player_scores[player1_id]}** | ' \
                      f'{player_scores[player2_id]} {user_ids[player2_id]}'
    else:
        final_score = f'{user_ids[player1_id]} {player_scores[player1_id]} | ' \
                      f'**{player_scores[player2_id]} {user_ids[player2_id]}**'

    embed = discord.Embed(
        title=match_title,
        url=match_link,
        colour=discord.Colour.magenta(),
        description=final_score
    )

    for score in match_scores:
        beatmap_title = score[0]
        player1_name = user_ids[score[1]]
        player1_score = int(score[2])
        player2_name = user_ids[score[3]]
        player2_score = int(score[4])

        if player1_score > player2_score:
            value_score = f'**{player1_name} {player1_score:,}** | {player2_score:,} {player2_name}'
        else:
            value_score = f'{player1_name} {player1_score:,} | **{player2_score:,} {player2_name}**'

        embed.add_field(name=beatmap_title, value=value_score, inline=False)

    thumbnail = 'https://cdn.discordapp.com/attachments/734824448137625731/734824581080285265/TheLogoFinal.png'
    embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=comments)

    await ctx.send(embed=embed)


client.run(TOKEN)
