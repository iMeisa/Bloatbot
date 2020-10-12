import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        await ctx.send(
            'You can check out https://github.com/iMeisa/Bloatbot/wiki/Bloatbot-Commands for my command page')


def setup(client):
    client.add_cog(Help(client))
