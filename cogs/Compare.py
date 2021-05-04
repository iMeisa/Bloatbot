from discord.ext import commands
import json
from util import osu


class Compare(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def c(self, ctx, *, user=''):
        if len(user) < 3:
            user = ctx.author.display_name

        with open('lib/recentbeatmaps.json', 'r') as f:
            recent_beatmaps = json.load(f)

        # Check if *r was used in the channel
        channel_id = str(ctx.channel.id)
        if channel_id not in recent_beatmaps:
            await ctx.send("Can't find recent map")
            raise ValueError

        beatmap_id = recent_beatmaps[channel_id]

        embed = osu.create_play_embed(user, beatmap_id=beatmap_id, channel_id=channel_id)

        if isinstance(embed, str):
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Compare(client))
