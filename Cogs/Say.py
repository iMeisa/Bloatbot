import discord
from discord.ext import commands


class Say(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def say(self, ctx, *, statement):
        await ctx.channel.purge(limit=1)
        await ctx.send(statement)


def setup(client):
    client.add_cog(Say(client))
