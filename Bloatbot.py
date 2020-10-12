from discord.ext import commands
from random import randint
import os

with open('token.txt', 'r') as fl:
    TOKEN = fl.read()
client = commands.Bot(command_prefix='*')
client.remove_command('help')

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')

bot_version = 'v1.7.2'


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
    if message.content.lower() == 'f' or ' died' in message.content.lower():
        if message.author.display_name != 'Bloatbot':
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

    if '<:angryasfuk:756187172230397973>' in message.content or 'fuck' in message.content.lower():
        if message.author.display_name != 'Bloatbot':
            await message.channel.send('<:angryasfuk:756187172230397973>')
    angry = randint(1, 1000) == 500
    if angry and message.author.display_name != 'Bloatbot':
        await message.channel.send('<:angryasfuk:756187172230397973>')
    else:
        await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pinged for {round(client.latency * 1000)}ms')


@client.command()
async def version(ctx):
    await ctx.send(bot_version)


@client.command()
async def invite(ctx):
    link = 'https://discord.com/api/oauth2/authorize?client_id=709553138977210381&permissions=1879960642&scope=bot'
    await ctx.send('Invite me to your server with this link: ' + link)


client.run(TOKEN)
