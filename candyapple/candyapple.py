import discord
from discord.ext import commands

class candyapple:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(candyapple(bot))