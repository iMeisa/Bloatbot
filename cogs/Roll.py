import discord
from discord.ext import commands
from random import randint


class Roll(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx, *, arg='string'):
        exists_arg = False

        # Default to *roll 100
        if arg == 'string':
            maximum = 100
        elif not arg.isdigit():
            maximum = 100
            exists_arg = True
        else:
            maximum = int(arg)

        # Roll with the value given (inclusive)
        max_range = int(maximum)
        number = randint(1, max_range + 1)
        if exists_arg:
            await ctx.send(f'{arg}: {number}')
        else:
            await ctx.send(f'{number} points')


def setup(client):
    client.add_cog(Roll(client))
