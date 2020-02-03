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
        for Member in ctx.message.mentions:
            await self.bot.send_message(Member.id)
        
        await self.bot.delete_message(ctx.message)
    
    def storage_get():
        return data
    
    def storage_set(data):
        return

def setup(bot):
    bot.add_cog(dayssince(bot))