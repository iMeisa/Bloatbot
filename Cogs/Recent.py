from discord.ext import commands
from Cogs.Tools import osu


class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def r(self, ctx, *, user_param=''):
        # Check if username is given
        def check_given_user(username):
            if len(username) < 3:
                checked_username = ctx.author.display_name
                return checked_username
            return username

        user = check_given_user(user_param)

        # Extract parameters
        beatmap_only = False
        show_all = False
        if user_param.startswith('-a ') or user_param.endswith('-a'):
            show_all = True
            user = check_given_user(osu.remove_param(user_param, '-a'))
        elif user_param.startswith('-b ') or user_param.endswith('-b'):
            beatmap_only = True
            user = check_given_user(osu.remove_param(user_param, '-b'))

        embed, praise = osu.create_play_embed(user, channel_id=ctx.channel.id,
                                              beatmap_only=beatmap_only, show_all=show_all)

        if isinstance(embed, str):
            await ctx.send(embed)
        else:
            await ctx.send(embed=embed)
            if praise is not None:
                await ctx.send(praise)


def setup(client):
    client.add_cog(Recent(client))
