from discord.ext import commands

from db.users import check_registration, register_user
from util.osu.api import get_user


class Register(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def register(self, ctx, osu_name: str):
        discord_id = str(ctx.author.id)

        registered = check_registration(discord_id)
        if registered:
            await ctx.send('You are already registered')
            return

        osu_id = get_user(osu_name).id
        registered = register_user(discord_id, osu_id)

        if registered:
            await ctx.message.add_reaction('✅')
            return

        await ctx.send("Couldn't register you for some reason")


def setup(client):
    client.add_cog(Register(client))
