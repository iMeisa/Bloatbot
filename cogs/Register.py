import json

from discord.ext import commands
from util.osu.api import get_user


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

        user = get_user(osu_name)
        users[author] = user.id

        with open('cache/users.json', 'w') as f:
            json.dump(users, f)

        await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Register(client))
