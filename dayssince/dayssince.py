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
        meltdown_embed = discord.Embed()
        meltdown_user = discord.Member

        if len(ctx.message.mentions) == 1:
            meltdown_user = ctx.message.mentions[0]
        else:
            meltdown_user = ctx.message.author
        
        meltdown_message = await self.bot.send_message(ctx.message.channel, embed=meltdown_embed)
        await self.bot.add_reaction(meltdown_message, discord.Emoji(ctx.message.guild.id, "dart"))

        while meltdown_message.reactions[0].count:
            if len(meltdown_message.reactions[0].count) > 1:
                print(meltdown_message.reactions)
                break

        await self.bot.delete_message(ctx.message)
    
    def storage_get():
        return data
    
    def storage_set(data):
        return

def setup(bot):
    bot.add_cog(dayssince(bot))