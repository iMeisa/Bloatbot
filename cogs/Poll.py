import discord
from discord.ext import commands


class Poll(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def poll(self, ctx, *, params):
        poll_letters = '🇦🇧🇨🇩'

        # Split based on quotes
        double_quotes = '"' in params
        if not double_quotes:
            options = params.split("'")
        else:
            options = params.split('"')

        for option in options:
            if option == ' ':
                options.remove(option)

        # Remove question from options
        options.pop(0)
        question = options[0]
        options.pop(0)
        option_count = len(options)

        # Add up all options to a single string
        poll_options = ''
        for i in range(option_count - 1):
            if i == len(poll_letters):
                break
            poll_options += f'{poll_letters[i]} {options[i]}\n'

        embed = discord.Embed(
            title=question,
            description=poll_options,
            color=discord.Color.blue()
        )

        msg = await ctx.send(embed=embed)
        for i in range(option_count - 1):
            await msg.add_reaction(poll_letters[i])


def setup(client):
    client.add_cog(Poll(client))
