import discord
from discord.ext import commands
import os

with open('keys/token.txt', 'r') as fl:
    TOKEN = fl.read()
client = commands.Bot(command_prefix='*')
client.remove_command('help')

for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_ready():
    print('Bloop bloop')
    await client.change_presence(status=discord.Status.online, activity=discord.Game('with dolphins'))

bot_version = 'v2.0-beta'


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.content.lower() in ['hi', 'hello', 'o/']:
        await message.channel.send('o/')

    if 'bloatbot' in message.content.lower():
        await message.channel.send(':blowfish:')

    if 'good bot' in message.content.lower():
        await message.channel.send(':D')

    if 'bad bot' in message.content.lower():
        await message.channel.send('D:')

    if message.content.lower().startswith('oof'):
        await message.channel.send('Oof')

    if message.content.lower() == 'nice' or '69' in message.content:
        await message.channel.send('Nice')

    if message.content.startswith('!r') or message.content.startswith('>rs'):
        await message.channel.send("You didn't use my *r command :(")

    if message.content.lower() == 'f':
        await message.channel.send('F')

    if ' tb ' in message.content.lower() or message.content.lower().startswith('tb hype'):
        await message.channel.send('TB HYPE')

    if 'good song' in message.content.lower():
        await message.channel.send(':notes:')

    if 'good enough' in message.content.lower():
        await message.channel.send(':thumbup:')

    if 'yay' in message.content.lower():
        await message.channel.send('\\o/')

    if message.content.lower().startswith('hm'):
        await message.channel.send('Hmmm')

    if message.content.lower().endswith('beast'):
        await message.channel.send('BEAST')

    if '<:angryasfuk:756187172230397973>' in message.content or 'fuck' in message.content.lower():
        await message.channel.send('<:angryasfuk:756187172230397973>')

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
