import discord
from discord.ext import commands
from random import randint
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import pickle
from ratelimit import limits, sleep_and_retry
from datetime import datetime

client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):

    if message.content.lower() in ['hi', 'hello']:
        await message.channel.send('o/')
    elif 'bloatbot' in message.content.lower():
        if message.author.display_name != 'Bloatbot':
            await message.channel.send(':blowfish:')
    elif 'good bot' in message.content.lower():
        await message.channel.send(':D')
    elif 'bad bot' in message.content.lower():
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
    if 'boatbot' in message.content.lower() or message.author.display_name == 'OsuBot':
        await message.channel.send(':sailboat:')
    if message.content.lower() == 'f' and message.author.display_name != 'Bloatbot':
        await message.channel.send('F')

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
async def dr(ctx, username='(username)'):
    await ctx.send("This command isn't currently functional")


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

# osu! API
with open('osuAPI.pickle', 'rb') as f:
    api_key = pickle.load(f)


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


def get_mods(mod_id):
    mod_id = int(mod_id)
    if mod_id == 0:
        return 'None'

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
        if i == (len(mod_list) - 1):
            used_mods += mod_list[i]
        else:
            used_mods += mod_list[i] + ', '

    return used_mods


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


@client.command()
async def r(ctx, *, user=''):
    if len(user) < 1:
        user = ctx.author.display_name
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
        await ctx.send(f"{user} hasn't played anything in a while")
    else:
        beatmap = user_recent[0]
        beatmap_data = get_beatmap_data(beatmap['beatmap_id'])
        beatmap_cover = 'https://assets.ppy.sh/beatmaps/' + beatmap_data['beatmapset_id'] + '/covers/cover.jpg'
        beatmap_title = f'{beatmap_data["artist"]} - {beatmap_data["title"]} [{beatmap_data["version"]}]'
        beatmap_link = 'https://osu.ppy.sh/b/' + beatmap['beatmap_id']
        beatmap_score = int(beatmap['score'])
        beatmap_diff = beatmap_data['difficultyrating'][:4]

        # Determine acc
        n0 = int(beatmap['countmiss'])
        n50 = int(beatmap['count50'])
        n100 = int(beatmap['count100'])
        n300 = int(beatmap['count300'])
        note_hit_count = (50 * n50) + (100 * n100) + (300 * n300)
        note_total = 300 * (n0 + n50 + n100 + n300)
        raw_acc = round((note_hit_count / note_total) * 10000)
        beatmap_acc = str(raw_acc / 100)
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
            title=beatmap_title,
            url=beatmap_link,
            description=f'**{beatmap_diff}**:star:',
            image=beatmap_cover
        )

        # Set embed color based on rank
        if beatmap['rank'] in ['SH', 'SSH']:
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
        embed.add_field(name=score_title, value=score_combo, inline=True)
        embed.add_field(name='Mods:', value=enabled_mods, inline=True)
        embed.set_image(url=beatmap_cover)
        embed.set_footer(text=time_diff)

        await ctx.send(embed=embed)


client.run('NzA5NTUzMTM4OTc3MjEwMzgx.Xrq7Rw.PwfD4TsmbqdB3vwIcmwf5MBvreU')
