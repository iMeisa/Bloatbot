from discord.ext import commands
import json
from Cogs.Tools import osu


class PlusMods(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def m(self, ctx, mods):
        with open('Cogs/Tools/recentbeatmaps.json', 'r') as f:
            recent_beatmaps = json.load(f)

        # Check if *r was used in the channel
        channel_id = str(ctx.channel.id)
        if channel_id not in recent_beatmaps:
            await ctx.send("Can't find recent map")
            raise ValueError

        beatmap_id = recent_beatmaps[channel_id]

        embed = osu.create_play_embed(user=ctx.author.display_name, beatmap_id=beatmap_id, beatmap_only=True, mods=mods)

        if isinstance(embed, str):
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PlusMods(client))
