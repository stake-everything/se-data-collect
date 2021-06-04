from etl import Etl
from collect import scrape_sites
import time

e = Etl()


def run():
    while True:
        scrape_sites(export=True)
        e.update_coins_db()
        e.update_historic_db()
        # time.sleep(60*60*60*24)
        time.sleep(10)


if __name__ == "__main__":
    run()
