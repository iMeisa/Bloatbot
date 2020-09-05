import discord
from discord.ext import commands
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import pickle
from ratelimit import limits, sleep_and_retry

with open('testtoken.txt', 'r') as fl:
    TOKEN = fl.read()
client = commands.Bot(command_prefix='*')

with open('osuAPI.pickle', 'rb') as fl:
    api_key = pickle.load(fl)


@client.event
async def on_ready():
    print('Bot is ready')


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


@client.command()
async def mp(ctx, match_link):
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

        score1 = game_scores[0]
        score2 = game_scores[1]
        user_id1 = score1['user_id']
        user_id2 = score2['user_id']

        if user_id1 not in player_scores:
            player_scores[user_id1] = 0
            player_scores[user_id2] = 0
            score1_username = get_user_data(user_id1)['username']
            user_ids[user_id1] = score1_username
            score2_username = get_user_data(user_id2)['username']
            user_ids[user_id2] = score2_username

        player1_score = score1['score']
        player2_score = score2['score']
        if player1_score > player2_score:
            player_scores[user_id1] += 1
        else:
            player_scores[user_id2] += 1

        beatmap_data = get_beatmap_data(beatmap_id)
        beatmap_title = f'{mappool[beatmap_id]}: {beatmap_data["artist"]} - {beatmap_data["title"]}'

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

    await ctx.send(embed=embed)


client.run(TOKEN)
