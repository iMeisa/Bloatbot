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


@client.command()
async def mp(ctx, match_link):
    match_url_split = match_link.split('/')
    match_id = match_url_split[-1]
    query = urlencode({'k': api_key, 'mp': match_id})
    url_params = 'get_match?' + query
    match_data = call_api(url_params)

    match_title = match_data['match']['name']
    match_games = match_data['games']

    embed = discord.Embed(
        title=match_title,
        url=match_link,
        colour=discord.Colour.magenta()
    )

    user_ids = {}
    for game in match_games:
        game_scores = game['scores']
        for score in game_scores:
            user_id = score['user_id']
            if user_id not in user_ids:
                score_username = get_user_data(user_id)['username']
                user_ids[user_id] = score_username
            embed.add_field(name=user_ids[user_id], value=score['score'], inline=True)

    thumbnail = 'https://cdn.discordapp.com/attachments/734824448137625731/734824581080285265/TheLogoFinal.png'
    embed.set_thumbnail(url=thumbnail)

    await ctx.send(embed=embed)


client.run(TOKEN)
