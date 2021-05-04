import json

from discord.ext import commands
from util import osu_api


class Register(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def register(self, ctx, osu_name):
        author = str(ctx.author.id)

        with open('cache/users.json', 'r') as f:
            users = json.load(f)
        if author in list(users.keys()):
            await ctx.send('You are already registered')
            return

        user = osu_api.get_user_data(osu_name)
        users[author] = user.user_id

        with open('cache/users.json', 'w') as f:
            json.dump(users, f)

        await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Register(client))
