import json

import discord
from discord.ext import commands
from util.osu_api import get_beatmap


class BeatmapDetails(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def b(self, ctx, map_id=None):
        if map_id is None:
            with open('cache/recentbeatmaps.json', 'r') as f:
                recent_beatmaps = json.load(f)

            channel_id = str(ctx.channel.id)
            if channel_id not in list(recent_beatmaps.keys()):
                await ctx.send('Provide beatmap id')
                return

            map_id = recent_beatmaps[channel_id]

        beatmap = get_beatmap(beatmap_id=map_id)

        embed = discord.Embed(

        )

        await ctx.send(beatmap.title)


def setup(client):
    client.add_cog(BeatmapDetails(client))
