from discord.ext import commands
from util import osu


class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nr(self, ctx):
        user = 'Meisa'  # While testing
        embed = osu.create_play_embed(user, channel_id=ctx.channel.id)

        if isinstance(embed, str):
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Recent(client))
