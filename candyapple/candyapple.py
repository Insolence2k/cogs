import discord
from discord.ext import commands

import os

class candyapple:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def test(self, ctx):
        await self.bot.say(ctx.message.channel, str(os.path.abspath(os.curdir)))

def setup(bot):
    bot.add_cog(candyapple(bot))