import discord

from classes.score import Score
from classes.user import User
from util.osu_tools import pp_calculation


def create_score_embed(user: User, score: Score) -> discord.Embed:
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
    embed.add_field(name='Mods:', value=score.enabled_mods_split, inline=True)
    embed.add_field(name='PP:', value=pp_value, inline=True)
    embed.set_image(url=score.beatmap.cover_url)
    embed.set_footer(text=score.when_played)

    return embed


def get_color(rank: str = 'F') -> discord.Color:
    rank = rank.upper()
    if rank in ['SH', 'SSH']:
        return discord.Color.light_grey()
    if rank in ['S', 'SS']:
        return discord.Color.gold()
    if rank == 'A':
        return discord.Color.green()
    if rank == 'B':
        return discord.Color.blue()
    if rank == 'C':
        return discord.Color.purple()
    if rank == 'D':
        return discord.Color.red()

    return discord.Color.darker_gray()
