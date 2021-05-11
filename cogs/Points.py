import discord
from discord.ext import commands

from db.points import get_points


class Points(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def p(self, ctx, member: discord.Member = None):
        discord_id = ctx.author.id
        discord_name = ctx.author.display_name
        if member is not None:
            discord_id = member.id
            discord_name = member.display_name

        point_total = get_points(discord_id)
        if point_total is None:
            await ctx.send(f"{discord_name} hasn't clicked circles yet")
            return

        embed = discord.Embed(
            title="Total",
            description=str(point_total) + ' circles',
            color=discord.Color.magenta()
        )
        embed.set_author(name=discord_name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def lb(self, ctx):
        pass


def setup(client):
    client.add_cog(Points(client))
