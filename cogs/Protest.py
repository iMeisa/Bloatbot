import discord
from discord.ext import commands


class Protest(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def protest(self, ctx):
        await ctx.send('<:angryasfuk:756187172230397973>')


def setup(client):
    client.add_cog(Protest(client))
