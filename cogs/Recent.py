import discord
from discord.ext import commands
import json

from util.embed_tools import get_color
from util.osu_api import get_recent_play, get_user
from util.osu_tools import pp_calculation, add_recent_beatmap


class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def r(self, ctx, username=None):
        if username is None:
            with open('cache/users.json', 'r') as f:
                users = json.load(f)

            author = str(ctx.author.id)
            if author not in list(users.keys()):
                await ctx.send('Who is you? Tell me who you are by doing *register `[your osu username]`')
                return

        user = get_user(username) if username is not None else get_user(users[str(ctx.author.id)], is_id=True)

        score = get_recent_play(user.id)
        if score is None:
            await ctx.send(f"{user.name} hasn't clicked circles in a while")
            return

        add_recent_beatmap(ctx.channel.id, score.beatmap_id)

        # Embed
        author = f'{user.name}: {user.pp:,}pp (#{user.global_rank:,} {user.country}{user.country_rank:,})'
        title = f'{score.beatmap.artist} - {score.beatmap.title} [{score.beatmap.version}]'
        description = f'**{score.beatmap.sr}** :star: '
        description += score.pass_amount if score.rank == 'F' else ''
        score_title = f'{score.score:,} ({score.acc})'
        score_combo = f'**{score.max_combo}x**/{score.beatmap.max_combo}X\n' \
                      f'{{ {score.count300} / {score.count100} / {score.count50} / {score.count_miss} }}'
        pp_max = pp_calculation(score.beatmap_id, mods=score.enabled_mods)
        pp_value = f'**{score.pp}pp**/{pp_max}PP'

        embed = discord.Embed(
            title=title,
            url=score.beatmap.url,
            description=description,
            colour=get_color(score.rank)
        )
        embed.set_author(name=author, icon_url=user.pfp, url=user.url)
        embed.add_field(name=score_title, value=score_combo, inline=True)
        embed.add_field(name='Mods:', value=score.enabled_mods, inline=True)
        embed.add_field(name='PP:', value=pp_value, inline=True)
        embed.set_image(url=score.beatmap.cover_url)
        embed.set_footer(text=score.when_played)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Recent(client))
