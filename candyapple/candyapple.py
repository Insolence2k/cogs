import discord
from discord.ext import commands
from redbot.core import data_manager
import os

class candyapple:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def test(self, ctx):
        await self.bot.send_message(ctx.message.channel, str(os.path.abspath(data_manager.cog_data_path(self))))

def setup(bot):
    bot.add_cog(candyapple(bot))