import discord
from discord.ext import commands
from urllib.request import urlopen
from urllib.parse import urlencode
import json
import pickle
from ratelimit import limits, sleep_and_retry
from datetime import datetime

with open('testtoken.txt', 'r') as fl:
    TOKEN = fl.read()
client = commands.Bot(command_prefix='*')


@client.event
async def on_ready():
    print('Bot is ready')


@client.event
async def on_message(message):
    print(message.content)

    await client.process_commands(message)


@client.command()
async def protest(ctx):
    await ctx.send('<:angryasfuk:756187172230397973>')


client.run(TOKEN)
