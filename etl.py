import json
import pyrebase
from collect import Scrape

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
            config_path = "../../"

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

                try:
                    d = {"site": self.DATA[tag][coin]["name"],
                         "url": self.DATA[tag][coin]["url"],
                         "apr": self.DATA[tag][coin]["apr"],
                         "apy": self.DATA[tag][coin]["apy"],
                         "token_earned": self.DATA[tag][coin]["earn"]
                         }
                    S.append(d)
                except KeyError:
                    pass

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

    def update_db(self):

        coins_list = self.get_coins()
        coins_dict = self.create_coins_dict(coins_list)
        self.db.update({"coins": coins_dict})


if __name__ == "__main__":

    etl = Etl()
    s = Scrape()

    # s.acryptos()
    s.bunny()
    s.auto()
    s.viking()
    s.goose()

    s.export()

    print(s.DATA)
    etl.update_db()
