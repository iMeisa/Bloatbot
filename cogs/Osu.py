import csv

import discord
from discord.ext import commands

from util.osu.api import get_user
from util.osu.tools import get_registered_user


class Osu(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def osu(self, ctx, username=None):
        user_id = None
        if username is None:
            user_id = get_registered_user(ctx.author.id)
            if user_id is None:
                await ctx.send('Who is you? Tell me who you are by doing *register `[your osu username]`')
                return

        user = get_user(username) if username is not None else get_user(user_id, is_id=True)

        # Country code reader
        with open('lib/country_codes.csv', 'r') as f:
            reader = csv.DictReader(f)
            country_codes = {}
            for row in reader:
                country_codes[row['alpha-2']] = row['name']
        country_name = country_codes[user.country.upper()]

        player_title = f'Stats for {user.name}\n'
        profile_stats = f'**Global Rank:** #{user.global_rank:,} (#{user.country_rank:,})\n' \
                        f''
        other_info = f'**Country:** :flag_{user.country.lower()}: {country_name}\n' \
                     f'**Join Date:** {user.join_date} UTC'

        embed = discord.Embed(
            color=discord.Color.red()
        )

        embed.set_author(name=player_title, url=user.url)
        embed.set_thumbnail(url=user.pfp)
        embed.add_field(name='__*Profile Stats:*__', value=profile_stats, inline=False)
        embed.add_field(name='__*Other Info:*__', value=other_info, inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Osu(client))
