from discord.ext import commands


class SomeClassName(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bug(self, ctx):
        ctx.send("If you have found a bug, please report it here: https://github.com/iMeisa/Bloatbot/issues/new")


def setup(client):
    client.add_cog(SomeClassName(client))
