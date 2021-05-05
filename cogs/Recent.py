from discord.ext import commands
import json

from util.embed_tools import create_score_embed
from util.osu_api import get_recent_play, get_user
from util.osu_tools import add_recent_beatmap


class Recent(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def r(self, ctx, username=None):
        if username is None:
            with open('cache/users.json', 'r') as f:
                users = json.load(f)

            author = str(ctx.author.id)
            if author not in list(users.keys()):
                await ctx.send('Who is you? Tell me who you are by doing *register `[your osu username]`')
                return

        user = get_user(username) if username is not None else get_user(users[str(ctx.author.id)], is_id=True)

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
