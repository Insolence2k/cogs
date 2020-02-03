import discord
import time
from discord.ext import commands

class dayssince:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def meltdown(self, ctx):
        """
        mono meltdown
        """
        meltdown_time = time.time()
        meltdown_embed = discord.Embed()
        meltdown_user = discord.Member

        if len(ctx.message.mentions) == 1:
            meltdown_user = ctx.message.mentions[0]
        else:
            meltdown_user = ctx.message.author
        
        meltdown_message = await self.bot.send_message(ctx.message.channel, embed=meltdown_embed)

        @self.bot.event
        async def on_reaction_add(reaction, user):
            if reaction.message.id == meltdown_message.id:
                if user == meltdown_user:
                    await self.bot.send_message(reaction.message.channel, "Hello!")

        await self.bot.delete_message(ctx.message)

        self.bot.on_

    def storage_get():
        return data
    
    def storage_set(data):
        return

def setup(bot):
    bot.add_cog(dayssince(bot))