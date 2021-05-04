from discord.ext import commands
from util import osu
import json


class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def nr(self, ctx):
        with open('cache/users.json', 'r') as f:
            users = json.load(f)

        author = str(ctx.author.id)
        if author not in list(users.keys()):
            await ctx.send('Who is you? Tell me who you are by doing *register `[your osu username]`')
            return
        user = json.load(f)[str(ctx.author.id)]

        embed = osu.create_play_embed(user, channel_id=ctx.channel.id)

        if isinstance(embed, str):
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Recent(client))
