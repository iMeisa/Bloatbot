import discord
from discord.ext import commands

from db.points import get_points, get_points_htl, change_points


class Points(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def p(self, ctx, member: discord.Member = None):
        discord_id = ctx.author.id
        discord_name = ctx.author.display_name
        if member is not None:
            discord_id = member.id
            discord_name = member.display_name

        point_total = get_points(discord_id)
        if point_total is None:
            await ctx.send(f"{discord_name} hasn't clicked circles yet")
            return

        embed = discord.Embed(
            title="Total",
            description=str(point_total) + ' circles',
            color=discord.Color.magenta()
        )
        embed.set_author(name=discord_name, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def give(self, ctx, amount: int, *members: discord.Member):
        for member in members:
            change_points(member.id, amount)

        await ctx.message.add_reaction('✅')

    @commands.command()
    async def lb(self, ctx, player_range=10):
        users = get_points_htl()
        guild = ctx.guild

        leaderboard = f'```{"RANK":<5} {"NAME":<32} {"POINTS":<6}```\n```'
        content_list = []
        rank = 1
        for user in users:
            user_id = int(user[0])
            points = user[1]

            member = guild.get_member(user_id)
            if member is None:
                continue

            rank_format = f'{str(rank) + ".":<5} {member.display_name:<32} {points:<6}'
            content_list.append(rank_format)

            if rank == player_range:
                break

            rank += 1

        leaderboard += '\n'.join(content_list) + '```'

        embed = discord.Embed(
            title='Leaderboard',
            description=leaderboard,
            color=discord.Color.magenta()
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Points(client))
