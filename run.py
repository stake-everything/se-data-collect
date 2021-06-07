from etl import Etl
from collect import scrape_sites
from helpers import Message
import time
import datetime
import sys

e = Etl()
m = Message()


def run():
    prod = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            prod = False
        elif sys.argv[1] == "run":
            prod = True

    while True:
        if prod == True:
            print("running...")
            try:
                if datetime.datetime.now().hour == 12:
                    print("Starting data collection...")
                    scrape_sites(_export=True)
                    print("site scrape finished. Updated database...")
                    e.update_coins_db()
                    print("Updating price database...")
                    e.update_historic_db()
                    print("Database updated. Sleeping...")
                    time.sleep(60*60*24 - 10)  # sleep one day minus 30 seconds

            except Exception as err:
                m.email("The following error was encountered:\n\n {}".format(err))
        else:
            print("testing...")
            print("Starting data collection...")
            scrape_sites(_export=True)
            print("site scrape finished. Updated database...")
            e.update_coins_db()
            print("Updating price database...")
            e.update_historic_db()
            print("Database updated. Sleeping...")
            time.sleep(60*5)


if __name__ == "__main__":

    run()
