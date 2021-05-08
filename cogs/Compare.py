from discord.ext import commands

from util.embed_tools import create_score_embed
from util.osu.api import get_user, get_user_map_best
from util.osu.tools import add_recent_beatmap, get_recent_beatmap, get_registered_user


class Compare(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def c(self, ctx, username=None):
        user_id = None
        if username is None:
            user_id = get_registered_user(ctx.author.id)
            if user_id is None:
                await ctx.send('Who is you? Tell me who you are by doing *register `[your osu username]`')
                return

        user = get_user(username) if username is not None else get_user(user_id, is_id=True)

        beatmap_id = get_recent_beatmap(ctx.channel.id)

        score = get_user_map_best(beatmap_id, user.id)
        if score is None:
            await ctx.send(f"{user.name} hasn't passed this map yet")
            return

        add_recent_beatmap(ctx.channel.id, score.beatmap_id)

        # Embed
        embed = create_score_embed(user, score)

        score_url = 'https://osu.ppy.sh/scores/osu/' + score.score_id
        embed.description += f' | **[View Score]({score_url})**'
        if score.replay_available:
            replay_download = score_url + '/download'
            embed.description += f' | **[Download Replay]({replay_download})**'

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Compare(client))
