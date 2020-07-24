from discord.ext import commands
from random import randint
import requests
import json

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

client.run('NzA5NTUzMTM4OTc3MjEwMzgx.Xrq7Rw.PwfD4TsmbqdB3vwIcmwf5MBvreU')
