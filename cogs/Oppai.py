import discord
from discord.ext import commands

from db.beatmaps import add_recent_beatmap, get_recent_beatmap
from util.osu import tools


class Oppai(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def oppai(self, ctx, *args):
        beatmap_id = None
        for arg in args:
            if arg.startswith('https://osu.ppy.sh/b'):
                beatmap_id = arg.split('/')[-1]
                args = args[1:]
                add_recent_beatmap(ctx.channel.id, beatmap_id)

        beatmap_id = get_recent_beatmap(ctx.channel.id) if beatmap_id is None else beatmap_id
        if beatmap_id is None:
            await ctx.send("No beatmaps have been posted on this channel yet")
            return

        output = tools.oppai(beatmap_id, ' '.join(args))

        oppai_description = output[5]
        star_rating = oppai_description.split()[0]
        desc = '**' + star_rating + '** :star: ' + oppai_description.split(' stars ')[-1]

        difficulty = output[2].split()
        hitwindow = output[3].split()[2]
        beatmap_difficulty = f'CS: `{difficulty[2][2:]}` AR: `{difficulty[0][2:]}`\n' \
                             f'OD: `{difficulty[1][2:]}` HP: `{difficulty[3][2:]}`\n' \
                             f'300 hitwindow: `{hitwindow}` ms'

        objects = output[4].split(', ')
        circle_count = objects[0].split()[0]
        slider_count = objects[1].split()[0]
        spinner_count = objects[2].split()[0]
        beatmap_objects = f'`{circle_count}` circles\n' \
                          f'`{slider_count}` sliders\n' \
                          f'`{spinner_count}` spinners'

        oppai_pp = output[10:12]
        stats = oppai_pp[0]
        max_pp, pp_strain = oppai_pp[1].split(' pp ')
        pp = f'{stats}\n' \
             f'{max_pp}pp\n' \
             f'{pp_strain}'

        oppai_strain = output[7:9]
        speed_strain = oppai_strain[0].split(': ')[-1]
        aim_strain = oppai_strain[1].split(': ')[-1]
        strain = f'Speed strain: `{speed_strain}`\n' \
                 f'▸Aim Strain: `{aim_strain}`'

        embed = discord.Embed(
            title=output[0],
            url='https://osu.ppy.sh/b' + beatmap_id,
            description=desc
        )
        embed.add_field(name='Difficulty', value=beatmap_difficulty)
        embed.add_field(name='Objects', value=beatmap_objects)
        embed.add_field(name='PP', value=pp)
        embed.add_field(name='Strain', value=strain, inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Oppai(client))
