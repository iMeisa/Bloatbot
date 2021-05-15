from discord import Embed, Color

from classes.score import Score
from classes.user import User
from util.osu.tools import pp_calculation


def create_score_embed(user: User, score: Score) -> Embed:
    """
    Creates discord embed from given `Score` class

    :param user: `User`
    :param score: `Score` achieved by user
    :return: Discord embed of `Score`
    """

    author = f'{user.name}: {user.pp:,}pp (#{user.global_rank:,} {user.country}{user.country_rank:,})'
    title = f'{score.beatmap.approved_emoji} {score.beatmap.artist} - {score.beatmap.title} [{score.beatmap.version}]'
    description = f'**{score.beatmap.sr}** :star: '
    description += score.pass_amount if score.rank == 'F' else ''
    score_title = f'{score.score:,} ({score.acc})'
    score_combo = f'**{score.max_combo}x**/{score.beatmap.max_combo}X\n' \
                  f'{{ {score.count300} / {score.count100} / {score.count50} / {score.count_miss} }}'
    pp_max = pp_calculation(score.beatmap_id, mods=score.enabled_mods)
    pp_value = f'**{score.pp}pp**/{pp_max}PP' if 0 < score.beatmap.approved <= 2 or score.rank == 'F' else \
        f'~~**{score.pp}pp**/{pp_max}PP~~'

    embed = Embed(
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


def get_color(rank: str = 'F') -> Color:
    """
    Gives `discord.Color` based on rank achieved in score

    :param rank: Rank achieved on score `str`
    :return: `discord.Color`
    """

    rank = rank.upper()
    if rank in ['SH', 'SSH']:
        return Color.light_grey()
    if rank in ['S', 'SS']:
        return Color.gold()
    if rank == 'A':
        return Color.green()
    if rank == 'B':
        return Color.blue()
    if rank == 'C':
        return Color.purple()
    if rank == 'D':
        return Color.red()

    return Color.darker_gray()
