from discord.ext import commands
from random import randint


class Choose(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def choose(self, ctx, *, arg=''):
        if ' or ' in arg:
            choices = arg.split(' or ')
            option = randint(1, 2)
            await ctx.send(choices[option])
        else:
            await ctx.send('Proper format: *choose (choice 1) or (choice 2)')


def setup(client):
    client.add_cog(Choose(client))
