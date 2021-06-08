from etl import Etl
from collect import scrape_sites
from helpers import Message
import time
import datetime
import sys
import logging


m2 = "Waiting for correct time. Sleeping for {} seconds"
m3 = "The following error was encountered: {}"
m4 = "Sending email"

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="_log.log",
                    level=logging.INFO,
                    format=LOG_FORMAT,
                    filemode="w")

logger = logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler())


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
            logger.info("Run started...")
            _time = datetime.datetime.now()
            try:
                if _time.hour == 12:
                    logger.info("Starting data collection...")
                    scrape_sites(_export=True)
                    logger.info("site scrape finished. Updated database...")
                    e.update_coins_db()
                    e.update_historic_db()
                    logger.info("Databases updated. Sleeping...")
                    time.sleep(60*60*24)  # sleep one day minus 30 seconds
                elif _time.hour > 12:
                    curr_second = 60*60*_time.hour + _time.minute*60 + _time.second
                    delta = 60*60*12*2 - curr_second
                    logger.info(m2.format(delta))
                    time.sleep(delta)

                elif _time.hour < 12:
                    12 - _time.hour
                    curr_second = 60*60*_time.hour + _time.minute*60 + _time.second
                    delta = 60*60*12 - curr_second
                    logger.info(m2.format(delta))
                    time.sleep(delta)

            except Exception as err:
                logger.info(m3.format(delta))
                logger.info(m4.format(delta))
                m.email("The following error was encountered:\n\n {}".format(err))
        else:
            logger.info("Test started...")
            logger.info("Starting data collection...")
            scrape_sites(_export=True)
            logger.info("site scrape finished. Updated database...")
            e.update_coins_db()
            e.update_historic_db()
            logger.info("Databases updated. Sleeping...")
            time.sleep(60*5)


if __name__ == "__main__":

    run()
