import json

import discord
from discord.ext import commands
from util.osu_api import get_beatmap
from util.osu_tools import pp_calculation, add_recent_beatmap
from util.time_format import sec_to_min, get_time_diff


class BeatmapDetails(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def b(self, ctx, *args):
        map_id = None
        mods = None
        for arg in args:
            if arg.startswith('https://osu.ppy.sh/b'):
                map_id = arg.split('/')[-1]
                add_recent_beatmap(ctx.channel.id, map_id)

            if arg.startswith('+'):
                mods = arg[1:]

        if map_id is None:
            with open('cache/recentbeatmaps.json', 'r') as f:
                recent_beatmaps = json.load(f)

            channel_id = str(ctx.channel.id)
            if channel_id not in list(recent_beatmaps.keys()):
                await ctx.send('Provide beatmap id')
                return

            map_id = recent_beatmaps[channel_id]

        beatmap = get_beatmap(beatmap_id=map_id)
        title = f'{beatmap.approved_emoji} {beatmap.artist} - {beatmap.title} [{beatmap.version}]'
        beatmap_cover = 'https://assets.ppy.sh/beatmaps/' + beatmap.set_id + '/covers/cover.jpg'
        beatmap_difficulty = f'CS: `{beatmap.cs}` AR: `{beatmap.ar}`\n' \
                             f'OD: `{beatmap.od}` HP: `{beatmap.hp}`'
        beatmap_time = f'{sec_to_min(beatmap.total_length)} ({sec_to_min(beatmap.hit_length)})'
        beatmap_info = f'Length: `{beatmap_time}\n`' \
                       f'BPM: `{int(beatmap.bpm)}`\n' \
                       f'Combo: `{beatmap.max_combo}`'

        pp_95 = pp_calculation(beatmap.id, mods=mods, percentage=95)
        pp_98 = pp_calculation(beatmap.id, mods=mods, percentage=98)
        pp_99 = pp_calculation(beatmap.id, mods=mods, percentage=99)
        pp_max = pp_calculation(beatmap.id, mods=mods)
        theoretical_pp = f'95%: `{pp_95}pp`\n98%: `{pp_98}pp`\n99%: `{pp_99}pp`\n100%: `{pp_max}pp`'

        upload_time_diff = get_time_diff(beatmap.approved_date)
        mapper_details = f'Mapped by {beatmap.mapper}, {beatmap.approved_status} {upload_time_diff}'
        mapper_pfp = 'https://a.ppy.sh/' + beatmap.mapper_id

        embed = discord.Embed(
            title=title,
            url=f'https://osu.ppy.sh/b/{beatmap.id}',
            description=f'**{beatmap.sr}** :star:',
            colour=discord.Color.teal()
        )
        embed.set_image(url=beatmap_cover)
        embed.add_field(name='Beatmap Difficulty', value=beatmap_difficulty, inline=True)
        embed.add_field(name='Beatmap Info', value=beatmap_info, inline=True)
        embed.add_field(name='PP Values:', value=theoretical_pp, inline=True)
        embed.set_footer(text=mapper_details, icon_url=mapper_pfp)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(BeatmapDetails(client))
