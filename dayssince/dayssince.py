import discord
import time
import json
import requests
from discord.ext import commands

jsonpool_auth = {
    "id":"rJC9jdBMU",
    "auth":"514429753e71887ae9aee0a0fc4beb9a"
}

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
        self.jp = JsonPool(jsonpool_auth["id"], jsonpool_auth["auth"])
        self.reaction = None

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
        (await self.bot.add_reaction(meltdown_message, self.reaction) if self.reaction else None)

        @self.bot.event
        async def on_reaction_add(reaction, user):
            if not self.reaction:
                self.reaction = reaction.emoji
            
            elif self.reaction:
                if not reaction.emoji == self.reaction:
                    return

            if reaction.message.id == meltdown_message.id:
                if user == meltdown_user:

                    if not self.reaction:
                        self.reaction = reaction

                    await self.bot.send_message(reaction.message.channel, "Hello!")
                    await meltdown_message.edit(embed=meltdown_embed)

        await self.bot.delete_message(ctx.message)

    def storage_get():
        return self.jp.get()
    
    def storage_set(data):
        return self.jp.update(data)

def setup(bot):
    bot.add_cog(dayssince(bot))