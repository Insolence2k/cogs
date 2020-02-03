import discord
import time
from dayssince.jsonpool import JsonPool
from discord.ext import commands

jsonpool_auth = {
    "id":"rJC9jdBMU",
    "auth":"514429753e71887ae9aee0a0fc4beb9a"
}

class dayssince:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.jp = JsonPool(jsonpool_auth["id"], jsonpool_auth["auth"])

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
        self.bot.add_reaction(meltdown_message, "dart")

        @self.bot.event
        async def on_reaction_add(reaction, user):
            if reaction.message.id == meltdown_message.id:
                if user == meltdown_user:
                    print(reaction)
                    await self.bot.send_message(reaction.message.channel, "Hello!")
                    await meltdown_message.edit(embed=meltdown_embed)

        await self.bot.delete_message(ctx.message)

    def storage_get():
        return self.jp.get()
    
    def storage_set(data):
        return self.jp.update(data)

def setup(bot):
    bot.add_cog(dayssince(bot))