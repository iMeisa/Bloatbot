# import discord
from discord.ext import commands
from random import randint


class Ask(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ask(self, ctx, *, question=None):
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

        if question is None:
            await ctx.send('Please ask a question')
        else:
            number = randint(0, len(responses) - 1)
            await ctx.send(responses[number])


def setup(client):
    client.add_cog(Ask(client))
