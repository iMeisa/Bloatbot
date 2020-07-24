from discord.ext import commands
from random import randint
import requests
from bs4 import BeautifulSoup as Soup
import json
from math import sqrt

client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    # with open('levels.json', 'r') as f:
    #     levels = json.load(f)

    # if message.author.display_name != 'Bloatbot':
    #     await update_data(levels, str(message.author.id))
    #     await add_exp(levels, str(message.author.id), 5)
    #     await level_up(levels, str(message.author.id), message.channel, message.author)

    if message.content.lower() in ['hi', 'hello']:
        await message.channel.send('o/')
    elif 'bloatbot' in message.content.lower():

        if message.author.display_name != 'Bloatbot':
            await message.channel.send(':blowfish:')
    elif 'good bot' in message.content or 'Good bot' in message.content:
        await message.channel.send(':D')
    elif 'bad bot' in message.content or 'Bad bot' in message.content:
        await message.channel.send('D:')

    if message.content.lower() == 'bot':
        await message.channel.send(':eyes:')
    if 'better' in message.content:
        await message.channel.send(':clap:')
    if message.content.lower().startswith('oof'):
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('Oof')
    if message.content == 'Nice' or '69' in message.content:
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('Nice')
    if 'boatbot' in message.content or 'Boatbot' in message.content or message.author.display_name == 'OsuBot':
        await message.channel.send(':sailboat:')
    if message.content.startswith('F') and message.content.endswith('F') and message.author.display_name != 'Bloatbot':
        await message.channel.send('F')

    # with open('levels.json', 'w') as f:
    #     json.dump(levels, f)

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


# async def update_data(levels, member):
#     if member not in levels:
#         levels[member] = {}
#         levels[member]['exp'] = 0
#         levels[member]['level'] = 0
#
#
# async def add_exp(levels, member, exp):
#     levels[member]['exp'] += exp
#
#
# async def level_up(levels, member, channel, user):
#     exp = levels[member]['exp']
#     lvl_start = levels[member]['level']
#     lvl_end = int(sqrt(exp / 100))
#
#     if lvl_start < lvl_end:
#         await channel.send(f'{user.mention} has leveled up to Bloatbot Level {lvl_end}!')
#
#     levels[member]['level'] = lvl_end


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


# @client.command()
# async def exp(ctx):
#     with open('levels.json', 'r') as f:
#         levels = json.load(f)
#
#     member_id = str(ctx.author.id)
#     await ctx.send(f'You have {levels[member_id]["exp"]} exp')


@client.command()
async def poke(ctx):
    if ctx.author.display_name != 'Bloatbot':
        await ctx.send('*poke')


# @client.command()
# async def level(ctx):
#     with open('levels.json', 'r') as f:
#         levels = json.load(f)
#
#     member_id = str(ctx.author.id)
#     await ctx.send(f'You are Bloatbot Level {levels[member_id]["level"]}')


# @client.command()
# async def nextlevel(ctx):
#     with open('levels.json', 'r') as f:
#         levels = json.load(f)
#
#     member_id = str(ctx.author.id)
#     current_level = levels[member_id]["level"]
#     current_exp = levels[member_id]["exp"]
#     exp_next_level = ((current_level + 1) ** 2) * 100
#     exp_current_level = (current_level ** 2) * 100
#     exp_progress = current_exp - exp_current_level
#     exp_required = exp_next_level - exp_progress
#
#     await ctx.send(f'You need {exp_required} more exp to level up')


# @client.command()
# async def showlevelcontents(ctx):
#     show_levels = open('levels.json', 'r').read()
#     author_id = str(ctx.author.id)
#     print(f'Looking for id: 353960679973191701\nYour id: {author_id}')
#     if author_id == '353960679973191701':
#         await ctx.send(show_levels)


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
    # if username == '(username)':
    #     await ctx.send('*dr (username)')
    # else:
    #     await ctx.send('Checking...')
    #     profile_url = f'https://osu.ppy.sh/u/{username}/osu'
    #
    #     response = requests.get(profile_url)
    #
    #     profile_soup = soup(response.text, 'html.parser')
    #     profile_html_json = profile_soup.find('script', id='json-user', type='application/json')
    #     profile_json_contents = profile_html_json.contents[0]
    #
    #     profile_dict = html_json_to_dict(profile_json_contents)
    #     rank_history = profile_dict['rankHistory']
    #     ranks = rank_history['data']
    #     rank_range = ranks[0] - ranks[-1]
    #
    #     if rank_range > 0:
    #         await ctx.send(f'{username} is not a deranker')
    #     elif rank_range < 0:
    #         await ctx.send(f'{username} is a deranker')
    #     else:
    #         await ctx.send('Unclear')
    await ctx.send("This command isn't currently functional")


@client.command()
async def rank(ctx, username='author'):
    if username == 'author':
        username = ctx.author.display_name
    profile_url = 'https://osu.ppy.sh/u/' + username + '/osu'

    response = requests.get(profile_url)

    # retrieves and parses JSON from HTML
    profile_soup = Soup(response.text, 'html.parser')
    player_html = profile_soup.find('script', id='json-user', type='application/json')
    player_info = str(player_html.contents[0])

    # finds the "global" tag
    global_rank_index = player_info.index('"global"')
    player_global_rank = player_info[global_rank_index + 9]

    # parses rank from "global" tag
    for i in range(10, 100):
        if player_info[global_rank_index + i].isdigit():
            player_global_rank += str(player_info[global_rank_index + i])
        else:
            break

    await ctx.send(f'{username} is rank {player_global_rank}')


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

client.run('NzA5NTUzMTM4OTc3MjEwMzgx.Xrq7Rw.PwfD4TsmbqdB3vwIcmwf5MBvreU')
