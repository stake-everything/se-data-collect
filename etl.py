import json
import pyrebase
from collect import Scrape
import time

"""
{"BUSD":[
    { "site":site,
      "url":url,
      "apr":apr,
      "apy":none,
      "token_earned":
     },
]}
"""


class Etl:

    def __init__(self, data_path=None, config_path=None):
        if data_path == None:
            data_path = ""
        if config_path == None:
            config_path = "../"

        with open(data_path+"data.json") as f:
            self.DATA = json.load(f)
        with open(data_path+"sites.json") as f:
            self.SITES = json.load(f)
        with open(data_path+"images.json") as f:
            self.IMAGES = json.load(f)
        with open(config_path+"config.json") as f:
            config = json.load(f)

        self.firebase = pyrebase.initialize_app(config['firebase'])
        self.db = self.firebase.database()

    def get_coins(self):
        tags = list(self.DATA.keys())
        coins = []
        for tag in tags:
            coins = coins+list(self.DATA[tag].keys())
        return list(set(coins))

    def create_coins_dict(self, coins_list):
        coins_dict = {}
        for coin in coins_list:
            tags = list(self.DATA.keys())

            S = []
            for tag in tags:
                _tag_coins = self.DATA[tag].keys()
                if coin in _tag_coins:
                    _data = self.DATA[tag][coin]
                    keys = _data.keys()

                    d = {"site": _data["name"],
                         "url": _data["url"],
                         "token_earned": _data["earn"]
                         }

                    if "apy" in list(_data.keys()):
                        d["apy"] = _data["apy"]
                    elif "apr" in list(_data.keys()):
                        d["apr"] = _data["apr"]

                    S.append(d)

            dtop = {"info": S}
            try:
                img_uri = self.IMAGES[coin]
                if img_uri == None:
                    img_uri = self.IMAGES["BNB"]
            except KeyError:
                img_uri = self.IMAGES["BNB"]

            dtop["image_uri"] = img_uri

            coins_dict[coin] = dtop

        return coins_dict

    def update_coins_db(self, over_write=False):
        coins_list = self.get_coins()
        coins_dict = self.create_coins_dict(coins_list)
        self.db.update({"coins": coins_dict})

    def update_historic_db(self):
        farm_tags = self.DATA.keys()

        hist = {}
        print(farm_tags)
        for tag in farm_tags:
            _tag_coins = self.DATA[tag].keys()
            for coin in _tag_coins:
                print(tag, coin)

                _coin_keys = self.DATA[tag][coin].keys()

                out = self.db.child("historic").child(
                    tag).child(coin).get().val()

                if out != None:
                    out = dict(out)
                    vals = out["values"]

                    if "apr" in _coin_keys:
                        vals.append(
                            self.DATA[tag][coin]["apr"])
                    elif "apy" in _coin_keys:
                        vals.append(
                            self.DATA[tag][coin]["apy"])

                    print(vals)

                    self.db.child("historic").child(
                        tag).child(coin).update({"t": out["t"].append(time.time())})

                    self.db.child("historic").child(tag).child(
                        coin).update({"values": vals})

                elif out == None:

                    newd = {"t": [time.time()]}
                    if "apr" in _coin_keys:
                        val = self.DATA[tag][coin]["apr"]
                    elif "apy" in _coin_keys:
                        val = self.DATA[tag][coin]["apy"]

                    if type(val) == float:
                        newd["values"] = [val]
                        self.db.child("historic").child(
                            tag).child(coin).set(newd)


if __name__ == "__main__":

    etl = Etl()
    # etl.update_coins_db()
    etl.update_historic_db()
