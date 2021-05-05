import discord


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
