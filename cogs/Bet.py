import discord
from discord.ext import commands

from db.bets import open_bet, add_bet, check_bets, check_users_participating, close_bet


class Bets(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def makebet(self, ctx, *, teams):
        bet_teams = teams.split(' vs ')
        team1 = bet_teams[0]
        team2 = bet_teams[1]

        active_bet = open_bet(ctx.channel.id, team1, team2)
        if active_bet is None:
            await ctx.message.add_reaction('✅')
            return

        current_bet = active_bet[0] + ' vs ' + active_bet[1]
        await ctx.send(f'There is already a bet on this channel: `{current_bet}`')

    @makebet.error
    async def makebet_error(self, ctx, error):
        await ctx.send('Use format *makebet `[team 1]` vs `[team 2]`')

    @commands.command()
    async def bet(self, ctx, bet_amount: int = None, *, team=None):
        response = add_bet(ctx.channel.id, ctx.author.id, bet_amount, team)

        if response is None:
            await ctx.message.add_reaction('✅')
            return

        await ctx.send(response)

    @commands.command()
    async def bets(self, ctx):
        bets = check_bets(ctx.channel.id)
        if bets is None:
            await ctx.send('No active bets on this channel rn, make a bet using *makebet `[team 1]` vs `[team 2]`')
            return

        current_bet = f'__{bets[0]}__ vs __{bets[1]}__'

        participating = check_users_participating(ctx.channel.id)

        guild = ctx.guild
        members = []
        for output in participating:
            discord_id = int(output[0])
            member = guild.get_member(discord_id)
            if member is not None:
                members.append(member.display_name)

        players = '\n'.join(members) if len(members) > 0 else 'None'

        embed = discord.Embed(
            title=current_bet,
            color=discord.Color.gold()
        )
        embed.add_field(name='Users', value=players)
        embed.set_author(name='Current Bet')

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def cancelbet(self, ctx):
        output = close_bet(ctx.channel.id, winning_team=None)
        await ctx.send(output)

    @commands.command()
    async def finishbet(self, ctx, *, winning_team):
        output = close_bet(ctx.channel.id, winning_team)
        await ctx.send(output)

    @finishbet.error
    async def finishbet_error(self, ctx, error):
        await ctx.send('Well? Who won?')


def setup(client):
    client.add_cog(Bets(client))
