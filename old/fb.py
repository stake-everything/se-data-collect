import pyrebase
import json
from helpers import scrape


class FirebaseAuth():
    def __init__(self):

        with open('../config.json') as f:
            config = json.load(f)

        self.firebase = pyrebase.initialize_app(config['firebase'])
        self.db = self.firebase.database()

    def upload_stocks_list(self, path=None, _list=True):

        if path:
            with open(path+'stocks_list.json') as f:
                sl = json.load(f)
        else:
            sl = scrape(exchange="all", save=False)

        if _list == True:
            self.db.update({"stocks": {"stocks-list": sl}})
        elif _list == False:
            for stock in sl:
                print(stock["ticker"])
                self.db.child("stocks").child(
                    "stocks-dict").child(stock["ticker"]).update(stock)


def get_db_data(_db, _tag):
    yout = _db.child(_tag).get()
    ym = max(list(yout.val()))
    return yout.val()[ym]


if __name__ == "__main__":

    fb = FirebaseAuth()
    db = fb.firebase.database()
    # print(db.child("reddit").child('1pm').set(
    #     [{"stock": "GME", "there": 6}, {"stock": "AMC", "there": 6}]))

    #fb.upload_stocks_list(path="../data/", _list=True)
    fb.upload_stocks_list(path="../data/", _list=False)

    #print(get_db_data(db, "yahoo"))
