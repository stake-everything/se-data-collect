import json
import pyrebase
from helpers import find
import time
import re


class Etl:

    def __init__(self, data_path=None, config_path=None):
        if data_path == None:
            self.data_path = ""
        if config_path == None:
            config_path = "../"

        # with open(data_path+"data.json") as f:
        #     self.DATA = json.load(f)
        with open(self.data_path+"sites.json") as f:
            self.SITES = json.load(f)
        with open(self.data_path+"images.json") as f:
            self.IMAGES = json.load(f)
        with open(config_path+"config.json") as f:
            config = json.load(f)

        self.firebase = pyrebase.initialize_app(config['firebase'])
        self.db = self.firebase.database()

    def get_coins(self):
        with open(self.data_path+"data.json") as f:
            self.DATA = json.load(f)

        tags = list(self.DATA.keys())
        coins = []
        for tag in tags:
            coins = coins+list(self.DATA[tag].keys())
        return list(set(coins))

    def create_coins_dict(self, coins_list):
        tokens = ["BTC", "BNB", "ETH", "BUSD", "ZEC", "ALPACA"]
        tokens = self.IMAGES.keys()
        reg_str = "^(\w+)({})$".format("|".join([t for t in tokens]))

        with open(self.data_path+"data.json") as f:
            self.DATA = json.load(f)

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
                         "token_earned": _data["earn"],
                         "tag": _data["tag"]
                         }

                    if "apy" in list(_data.keys()):
                        d["apy"] = _data["apy"]
                    elif "apr" in list(_data.keys()):
                        d["apr"] = _data["apr"]

                    S.append(d)

            dtop = {"info": S}

            img_coin = coin

            if re.search(reg_str, coin):
                img_coin = find(coin, tokens)
                #print(coin, img_coin)

            try:
                img_uri = self.IMAGES[img_coin]
                if img_uri == None:
                    img_uri = self.IMAGES["BNB"]
            except KeyError:
                img_uri = self.IMAGES["BNB"]

            dtop["image_uri"] = img_uri

            coins_dict[coin] = dtop

        return coins_dict

    def update_coins_db(self):
        coins_list = self.get_coins()
        coins_dict = self.create_coins_dict(coins_list)
        self.db.update({"coins": coins_dict})

    def update_historic_db(self):
        with open(self.data_path+"data.json") as f:
            self.DATA = json.load(f)

        farm_tags = self.DATA.keys()

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
                    t = out["t"]
                    t.append(time.time())

                    if "apr" in _coin_keys:
                        vals.append(
                            self.DATA[tag][coin]["apr"])
                    elif "apy" in _coin_keys:
                        vals.append(
                            self.DATA[tag][coin]["apy"])

                    self.db.child("historic").child(
                        tag).child(coin).update({"t": t})

                    self.db.child("historic").child(tag).child(
                        coin).update({"values": vals})

                elif out == None:

                    print("in out none")

                    if "apr" in _coin_keys:
                        val = self.DATA[tag][coin]["apr"]
                    elif "apy" in _coin_keys:
                        val = self.DATA[tag][coin]["apy"]

                    if type(val) == float:
                        newd = {"t": [time.time()], "values": [val]}

                        print(newd)

                        self.db.child("historic").child(
                            tag).child(coin).set(newd)


if __name__ == "__main__":

    e = Etl()
    e.update_coins_db()
