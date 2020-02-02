import discord
from discord.ext import commands

class dayssince:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def meltdown(self, ctx):
        """
        mono meltdown
        """
        return
    
def setup(bot):
    bot.add_cog(dayssince(bot))