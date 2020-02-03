import discord
import time
import json
import requests
import math
from discord.ext import commands

"""
class JsonPool
dynamic JsonPool object for communication with a jsonpool service

@param pool_id: JsonPool pool id, if the pool is public and only the id is suplied then JsonPool is read only
@param auth: Auth used for writing/updating pools and for reading private pools
@param private: Only used if creating new pool, makes it private. Default 1.
@param api_endpoint: /pool endpoint for JsonPool service default is the publicly hosted one.

"""
class JsonPool:
    # default endpoint
    api_endpoint = "https://jsonpool.herokuapp.com/pool/"

    def __init__(self, pool_id = None, auth = None, private = 1, api_endpoint = None):
        # Set a different endpoint if required
        if api_endpoint:
            self.api_endpoint = api_endpoint

        # Try read only mode
        if pool_id and not auth:
            self.id = pool_id

            if not self.exists():
                raise Exception("pool {} does not exist or it is private.".format(self.id))

        elif pool_id and auth:
            self.id = pool_id
            self.auth = auth

        else:
            req = requests.post(self.api_endpoint + "?private=1" if private else "")
            res = json.loads(req.text)
            if req.status_code == 200 and "auth" in res.keys():
                self.id = res["id"]
                self.auth = res["auth"]
            else:
                raise Exception("Failed to create a new pool")
    
    def get(self):
        req = requests.get(self.api_endpoint + self.id + "?auth={}".format(self.auth) if self.auth else "")
        
        if req.status_code == 200:
            return json.loads(req.text)
        else:
            return False
    
    def update(self, new, override = True):
        req = requests.put(self.api_endpoint + self.id, data=json.dumps({
            "id":self.id,
            "auth":self.auth,
            "data":new,
            "override":override
        }), headers={
            "Content-Type":"application/json"
        })

        res = json.loads(req.text)

        if req.status_code == 200 and res["status"] == "ok":
            return True
        else:
            return False
    
    def delete(self):
        req = requests.delete(self.api_endpoint + self.id + "?auth={}".format(self.auth))

        res = json.loads(req.text)

        if req.status_code == 200 and res["status"] == "ok":
            self.id = ""
            self.auth = ""
            return True
        else:
            return False

    """
    Check if pool is public/acceseble/exists
    """
    def exists(self):
        return requests.get(self.api_endpoint + self.id).status_code != 500

class dayssince:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.jp = lambda: JsonPool("HkRHdsBfU", "7b4a90a2aa2ef1129da15a527b65b349")
        self.reaction = None

    @commands.command(pass_context=True)
    async def meltdown(self, ctx):
        """
        mono meltdown
        """
        global meltdown_stats
        meltdown_stats = self.jp().get()
        
        meltdown_user = discord.Member

        if len(ctx.message.mentions) == 1:
            meltdown_user = ctx.message.mentions[0]
        else:
            meltdown_user = ctx.message.author
    
        meltdown_message = await self.bot.send_message(ctx.message.channel, embed=self.make_embed(meltdown_user, meltdown_stats))
        (await self.bot.add_reaction(meltdown_message, self.reaction) if self.reaction else None)

        @self.bot.event
        async def on_reaction_add(reaction, user):
            print(meltdown_stats)

            if not self.reaction:
                self.reaction = reaction.emoji

            if reaction.message.id == meltdown_message.id:
                if user == meltdown_user:
                    if not self.reaction:
                        self.reaction = reaction
                    # meltdown_stats = self.jp.get()
                    meltdown_stats[str(user.id)] = meltdown_stats[str(user.id)] if str(user.id) in meltdown_stats.keys() else {}
                    meltdown_stats[str(user.id)]["m"] = time.time()
                    meltdown_stats[str(user.id)]["c"] = 1 + (meltdown_stats[str(user.id)]["c"] if "c" in meltdown_stats[str(user.id)].keys() else 0)

                    self.jp().update(meltdown_stats)
                    new_embed = self.make_embed(meltdown_stats, meltdown_user)

                    await self.bot.edit_message(reaction.message, embed=new_embed)
                    await reaction.message.edit(embed=new_embed)

        await self.bot.delete_message(ctx.message)

    def make_embed(self, meltdown_user, meltdown_stats):
        meltdown_embed = discord.Embed()
        meltdown_embed.title = "Last meltdown for {}".format(str(meltdown_user))
        meltdown_user_stats = meltdown_stats[str(meltdown_user.id)] if str(meltdown_user.id) in meltdown_stats.keys() else None
        meltdown_embed.description = "{} days ago.\n {} meltdowns so far".format(str(math.floor((time.time() - meltdown_user_stats["m"]) / 60 / 60 / 24)), str(meltdown_user_stats["c"])) if meltdown_user_stats else "No meltdowns!"
        return meltdown_embed

def setup(bot):
    bot.add_cog(dayssince(bot))