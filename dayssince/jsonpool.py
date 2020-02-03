import json
import requests

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

 