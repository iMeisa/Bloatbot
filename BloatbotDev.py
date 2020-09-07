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


@client.command()
async def poll(ctx, *, params):
    poll_letters = 'abcdefghijklmnopqrstuvwxyz'
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
        question += f'\n:regional_indicator_{poll_letters[i]}: {options[i]}'

    await ctx.send(question)
    print(options)


client.run(TOKEN)
