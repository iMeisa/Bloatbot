import discord
from discord.ext import commands
from random import randint

from db.points import get_points, change_points


class Gambling(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coin(self, ctx, *args):
        discord_id = ctx.author.id

        heads_logo = ctx.author.avatar_url
        tails_logo = "https://upload.wikimedia.org/wikipedia/commons/e/e3/Osulogo.png"

        bet = 10
        choice_heads = True
        for arg in args:
            arg = str(arg)

            if arg.isdigit():
                bet = int(arg)

            if arg in 'tails':
                choice_heads = False

        user_points = get_points(discord_id)
        user_points = 0 if user_points is None else user_points
        if user_points < bet:
            await ctx.send(f"You only have {user_points} circles")
            return

        heads = randint(0, 1) == 0

        coin_value = 'Heads' if heads else 'Tails'
        win = choice_heads == heads

        if win:
            change_points(discord_id, bet)

        embed = discord.Embed(
            title="Coin Toss",
            color=discord.Color.teal(),
            description=coin_value
        )

        embed.set_thumbnail(url=heads_logo if heads else tails_logo)
        embed.add_field(name='Win!' if win else 'Lose!', value=str(bet if win else -bet))

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Gambling(client))
