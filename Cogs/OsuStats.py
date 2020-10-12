import discord
from discord.ext import commands
from Cogs.Tools import osu


class OsuStats(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def osu(self, ctx, *, raw_user=None):
        user = raw_user
        if raw_user is None:
            user = ctx.author.display_name

        user_data = osu.get_user_data(user)
        user_pfp = 'https://a.ppy.sh/' + user_data['user_id']
        username = user_data['username']
        user_url = 'https://osu.ppy.sh/u/' + user
        global_rank = user_data['pp_rank']
        embed_title = 'Global Rank: ' + global_rank

        embed = discord.Embed(
            title=embed_title
        )

        embed.set_author(name=username, icon_url=user_pfp, url=user_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(OsuStats(client))
