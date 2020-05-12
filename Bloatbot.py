import discord
from discord.ext import commands
from random import randint
import requests
from bs4 import BeautifulSoup as soup
import json


def html_json_to_dict(json_contents):
    # removes first 8 spaces
    json_file = ''
    for i in range(9, len(json_contents)):
        json_file += json_contents[i]

    # makes json into dict
    return json.loads(json_file)


client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    if message.content.startswith('hi') or message.content.startswith('hello') \
            or message.content.startswith('Hi') or message.content.startswith('Hello'):
        await message.channel.send('o/')
    elif 'good bot' in message.content or 'Good bot' in message.content:
        read_praise = open('praise.txt', 'r').read()
        praise_count = int(read_praise)
        write_praise = open('praise.txt', 'w')
        await message.channel.send(':D')
        write_praise.write(str(praise_count + 1))
        write_praise.close()
    elif 'bad bot' in message.content or 'Bad bot' in message.content:
        await message.channel.send('D:')
    elif 'bot' in message.content:
        await message.channel.send(':eyes:')

    if 'better' in message.content:
        await message.channel.send(':clap:')
    if 'Oof' in message.content and message.author.display_name != Bloatbot:
        await message.channel.send('Oof')
    if 'covid-19' in message.content or 'Covid-19' in message.content:
        await message.channel.send('No comment')

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pinged for {round(client.latency * 1000)}ms')


@client.command()
async def hi(ctx):
    author = str(ctx.author)
    await ctx.send(f'o/ {author[: -5]}')


@client.command()
async def goodbot(ctx):
    read_praise = open('praise.txt', 'r').read()
    praise_count = int(read_praise)
    write_praise = open('praise.txt', 'w')
    await ctx.send(':D')
    write_praise.write(str(praise_count + 1))
    write_praise.close()


@client.command()
async def praisecount(ctx):
    read_praise = open('praise.txt', 'r').read()
    praise_count = int(read_praise)
    await ctx.send(f'I have been praised {praise_count} times')


@client.command()
async def badbot(ctx):
    await ctx.send('D:')


@client.command()
async def osu(ctx):
    await ctx.send('Click the circles!')


@client.command()
async def roll(ctx, maximum='string'):
    if not maximum.isdigit():
        maximum = 100
    max_range = int(maximum)
    await ctx.send(f'{randint(1, max_range + 1)}')


@client.command()
async def dr(ctx, username='(username)'):
    if username == '(username)':
        await ctx.send('*dr (username)')
    else:
        await ctx.send('Checking...')
        profile_url = f'https://osu.ppy.sh/u/{username}/osu'

        response = requests.get(profile_url)

        profile_soup = soup(response.text, 'html.parser')
        profile_html_json = profile_soup.find('script', id='json-user', type='application/json')
        profile_json_contents = profile_html_json.contents[0]

        profile_dict = html_json_to_dict(profile_json_contents)
        rank_history = profile_dict['rankHistory']
        ranks = rank_history['data']
        rank_range = ranks[0] - ranks[-1]

        if rank_range > 0:
            await ctx.send(f'{username} is not a deranker')
        elif rank_range < 0:
            await ctx.send(f'{username} is a deranker')
        else:
            await ctx.send('Unclear')


@client.command()
async def mirairanks(ctx):
    await ctx.send('This may take a while...')
    teams = [['Rusty Cucumber', 'RevRoadster', 'ShadowDrake77', 'Shrukaghn', 'ruruchewy'],
             ['Sotarks One Tricks', 'Frostdogspd', 'matthiaslai'],
             ['shaky hand', 'Fallen_HK', 'Himman', 'McFuddyDuddy', 'Player01'],
             ['cherry gum v4', 'steve04', 'DanX', 'ABKirito'],
             ['Uprankers', 'Sonic-', 'Loreal', 'DanielSiew', 'Kumaxione'],
             ['Rip OsumeWolf', 'ErroTheCube', 'ISpiritI', 'stefgast13', 'Miles_Naismith'],
             ['kamiguozi', 'Guozi on Osu', 'na-gi', 'Mars New', '- Rainbow -'],
             ['surprised_pikachu', '-Secured-', 'Pokeinfernape', '7heGh0st', 'Emfyr'],
             ['The', 'Meisa', 'Aupsie', 'de_end'],
             ['Norank MaMa <3 U', 'Mangent', 'Dnwings', 'Muziyami', 'osu happy'],
             ['How2NoMod', '-Flux', 'Ostiminum', 'das12344321', 'MylerMoss'],
             ['Retirement Home', 'Redavor', 'DerNettePanda', 'Endaris', 'Shovan'],
             ['Airline Food', 'Shawn -', 'NekoMeganG', 'Champs de ble', 'Pythia'],
             ['im pepa gpig', 'Nova Cobalt', 'fw8te', 'CrappySalami'],
             ['HappyHuskyBubbles', 'MatthewBubbles', 'Harpiness', 'huskaii', 'onyo'],
             ['WorldWide Bootleg', 'Zack228752', 'FlagFlayer'],
             ['Baeguette', 'pauloreb28', 'Hyuras'],
             ['Nice Nice Nice', 'AntiButter', 'MonkeyyHug', 'xix'],
             ['Salted_Fish', 'lontom00126', 'WIFIxFTT', 'wanwan4343'],
             ['Team Sliderbreak', 'ethangrieve1', 'tronald-', '- cry -', 'Kiing'],
             ['8 min tech map', 'poboi06', 'SirPinky', 'meapii', 'His'],
             ['bee movie 2 2', 'PM ME YUR MEMES', 'rhythm on osu'],
             ['Nanahira Copypasta', 'Synchyy', 'Coradi', 'SillySoon', 'Poke7z'],
             ['bruh moment', 'TankoDen', 'eFrostBite', 'TMrex'],
             ['Tempe', 'Darctuile', 'Mer C'],
             ['WhamDabbFTW', 'MeiFTW', 'Nambulance', 'Maki-kun', 'AO4ILukas'],
             ['Makowy', 'Milkowy', '[LUX]Makushi'],
             ['FastButNotFurious', 'Sirek', 'Hiterzajc'],
             ['LowAcc Players', 'Eg2nD', 'ButterJelly'],
             ['Baka gang.', 'Yote', 'Avenger284', 'DeathByDarwin'],
             ['Your Average Team', 'Isterix', 'Meramipop'],
             ['Bokeee', 'vectorgas', 'ivoturi']]
    team_rank = []
    players = []

    def get_rank(username):
        # generates url for given name
        profile_url = 'https://osu.ppy.sh/u/' + username + '/osu'

        response = requests.get(profile_url)

        # retrieves and parses JSON from HTML
        profile_soup = soup(response.text, 'html.parser')
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

        return player_global_rank

    # gets rank from each player
    for team in teams:
        print(f'{team[0]}:')
        team_total_rank = 0
        for player in range(1, len(team)):
            player_name = team[player]
            player_rank = get_rank(player_name)
            print(f'\t{player_name}: {player_rank}')
            if player_rank.isdigit():
                team_total_rank += int(player_rank)
                players.append(player_name)
                players.append(int(player_rank))
        team_average_rank = team_total_rank // (len(team) - 1)
        team_rank.append(team_average_rank)
        print(f'Team average: {team_average_rank}\n')

    # ranks each team by average rank
    team_ranks = ''
    team_print_count = 1
    for rank in range(200000):
        if rank in team_rank:
            team_index = team_rank.index(rank)
            team = teams[team_index]
            team_name = team[0]
            team_status = f'{team_print_count}. {team_name}: {rank}\n'
            if (len(team_ranks) + len(team_status)) < 2000:
                team_ranks += team_status
            else:
                await ctx.send(team_ranks)
                team_ranks = ''
            # print(team_status)
            team_print_count += 1
    await ctx.send(team_ranks)

    # ranks each player by rank
    player_ranks = ''
    player_print_count = 1
    for rank in range(110000):
        if rank in players:
            name_index = players.index(rank) - 1
            player_name = players[name_index]
            player_status = f'{player_print_count}. {player_name}: {rank}\n'
            if (len(player_ranks) + len(player_status)) < 2000:
                player_ranks += player_status
            else:
                await ctx.send(player_ranks)
                player_ranks = ''
            # print(player_status)
            player_print_count += 1
    await ctx.send(player_ranks)


@client.command()
async def rank(ctx, username):
    profile_url = 'https://osu.ppy.sh/u/' + username + '/osu'

    response = requests.get(profile_url)

    # retrieves and parses JSON from HTML
    profile_soup = soup(response.text, 'html.parser')
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


client.run('NzA5NTUzMTM4OTc3MjEwMzgx.Xrq7Rw.PwfD4TsmbqdB3vwIcmwf5MBvreU')
