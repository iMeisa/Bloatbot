from discord.ext import commands

from db.beatmaps import add_recent_beatmap
from db.users import get_registered_user
from util.embed_tools import create_score_embed
from util.osu.api import get_recent_play, get_user


class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def r(self, ctx, username=None):
        user_id = None
        if username is None:
            user_id = get_registered_user(ctx.author.id)
            if user_id is None:
                await ctx.send('Who is you? Tell me who you are by doing *register `[your osu username]`')
                return

        user = get_user(username) if username is not None else get_user(user_id, is_id=True)

        score = get_recent_play(user.id)
        if score is None:
            await ctx.send(f"{user.name} hasn't clicked circles in a while")
            return

        add_recent_beatmap(ctx.channel.id, score.beatmap_id)

        # Embed
        embed = create_score_embed(user, score)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Recent(client))
