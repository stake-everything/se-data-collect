from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
import os
import requests
import yaml
from helpers import scroll_down_all, replace, Message
import re
from retry import retry
import logging


logger = logging.getLogger(__name__)
os.environ['MOZ_HEADLESS'] = '1'
m = Message()


def update_data(site_data, coin, earn, earn_perc, name, url, tag):

    def parse_perc(p):
        try:
            if p.find("K") != -1:
                return float(p.replace("K", "").replace("%", ""))*1000
            else:
                return float(earn_perc[1].replace("%", ""))
        except ValueError:
            return None

    site_data[coin] = {
        "stake": coin,
        "earn": earn,
        "name": name,
        "url": url,
        "tag": tag
    }
    site_data[coin][earn_perc[0]] = parse_perc(earn_perc[1])


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def auto(soup, name, url, tag):
    IGNORE = []
    EARN_TYPE = "apy"

    main_el = {"type": "div",
               "class": "text-left text-sm sm:text-base py-2 px-4 bg-opacity-50 hover:bg-opacity-100 dark:hover:bg-gray-800 bg-gray-100 dark:bg-gray-900 rounded-lg"
               }

    coin_el = {"type": "div",
               "class": "font-display"
               }

    earn_el = {"type": "div",
               "class": "items-center text-gray-500 dark:text-gray-400 font-medium text-xs sm:text-sm"
               }

    perc_el = {"type": "div",
               "class": "font-display text-sm sm:text-base"
               }

    tdivs = soup.find_all(main_el["type"], {"class": main_el["class"]})

    # test code
    # print(tdivs[0].find(coin_el["type"], {
    #       "class": coin_el["class"]}).text)
    # print(tdivs[0].find(earn_el["type"], {
    #       "class": earn_el["class"]}).find_all("div")[0].text)
    # print(tdivs[0].find(perc_el["type"], {"class": perc_el["class"]}).text)

    # print(jim)

    site_data = {}
    for tdiv in tdivs:

        coin = tdiv.find(coin_el["type"], {"class": coin_el["class"]}).text

        if coin.find("-") != -1 or coin in IGNORE:
            pass
        else:
            # coin = coin.replace("belt", "").replace("i", "")

            # get earn and earn_perc (%)
            earn = tdiv.find(earn_el["type"], {
                             "class": earn_el["class"]}).find_all("div")[0].text
            earn_perc = tdiv.find(
                perc_el["type"], {"class": perc_el["class"]}).text

            update_data(site_data, coin, earn,
                        (EARN_TYPE, earn_perc), name, url, tag)

    return site_data


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def jetfuel(soup, name, url, tag):
    IGNORE = []
    EARN_TYPE = "apy"

    tdivs = soup.find_all(
        "div", {"class": "vaults-page-single-item-wrapper"})

    """test code"""
    # tinfo = tdivs[3].find_all("div", {"class": "token-info"})

    # coin = tinfo[0].find(
    #     "div", {"class": "token-name"}).text.strip()
    # earn = tinfo[1].find(
    #     "div", {"class": "token-name"}).text.strip()

    # perc_text = tdivs[0].find("div", {"class": "apy"}).text.strip()
    # apy = tdivs[0].find(
    #     "div", {"class": "percentage"}).text

    site_data = {}
    for tdiv in tdivs:

        tinfo = tdiv.find_all("div", {"class": "token-info"})

        coin = tinfo[0].find(
            "div", {"class": "token-name"}).text.strip()
        earn = tinfo[1].find(
            "div", {"class": "token-name"}).text.strip()

        if coin.find("-") != -1 or coin in IGNORE:
            pass
        else:

            perc_text = tdivs[0].find("div", {"class": "apy"}).text.strip()
            apy = tdivs[0].find(
                "div", {"class": "perc-value"}).text

            earn_perc = (EARN_TYPE, apy)

            update_data(site_data, coin, earn, earn_perc,
                        name, url, tag)

    return site_data


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def beefy(name, url, tag):
    IGNORE = ["3EPS", "4BELT"]
    tokens = ["BTC", "BNB", "ETH", "BUSD", "ZEC", "ALPACA"]

    reg_str = "^(\w+)({})$".format("|".join([t.lower() for t in tokens]))

    page = requests.get(
        "https://github.com/beefyfinance/beefy-api/tree/master/src/api/stats/bsc")

    soup = BeautifulSoup(page.content, "lxml")
    j = requests.get("https://api.beefy.finance/apy").json()

    a_s = soup.find_all("a", {"class": "js-navigation-open Link--primary"})
    farms = [a.text.strip() for a in a_s[:-1]]

    site_data = {}
    for pair in list(j.keys()):
        if pair.count("-") == 1:
            farm = pair[:pair.find("-")]
            coin = pair[pair.find("-")+1:]

            if re.search(reg_str, coin) == None:
                coin = coin.upper()
            elif re.search(reg_str, coin):
                coin = replace(coin, tokens)

            if farm in farms and coin not in IGNORE:

                rate = str(round(j[pair]*10, 2)) if j[pair] != None else "None"

                update_data(site_data, coin, coin,
                            ("apy", rate), name, url, tag)

    return site_data


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def bunny(soup, name, url, tag):
    IGNORE = []
    EARN_TYPE = "apy"

    tdivs = soup.find_all("div", {"class": "row"})

    site_data = {}
    for tdiv in tdivs[1:]:

        coin = tdiv.find(
            "div", {"class": "label"}).find_all("span")[0].text

        if coin.find("-") != -1 or coin in IGNORE:
            pass
        else:

            apy = tdiv.find(
                "div", {"class": "rates"}).find_all("span")[0].text
            earn_perc = (EARN_TYPE, apy)

            earn = tdiv.find("div", {"class": "details return"}).find_all(
                "span", {"class": "value"})[0].text

            update_data(site_data, coin, earn, earn_perc,
                        name, url, tag)

    return site_data


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def viking(soup, name, url, tag):
    IGNORE = []

    tdivs = soup.find_all("div", {"class": "sc-ikPAkQ diwHUn"})
    site_data = {}
    for tdiv in tdivs:

        coin = tdiv.find(
            "h2", {"class": "sc-gsTCUz sc-idOhPF lbFLsG lnUPhx"}).text

        if coin.find("-") != -1 or coin in IGNORE:
            pass

        else:

            apr = tdiv.find("div", {"class": "sc-gsTCUz cBbMuj"}).text
            earn = tdiv.find("div", {"class": "sc-eCssSg MoQXc"}
                             ).find("div", {"class": "sc-gsTCUz cBbMuj"}).text

            earn_perc = ("apr", apr)

            update_data(site_data, coin, earn, earn_perc, name, url, tag)

    return site_data


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def acryptos(soup, name, url, tag):
    IGNORE = ["A2B2", "ACS3", 'ACS3BTC', 'ACS4USD', 'ACS4VAI', 'ACS4UST']

    def get_earn(tdiv):
        try:
            get_text = tdiv.find("span", {"class": "wallet-info"}).text
            get_text = get_text[:get_text.find(":")]
            earn = get_text.replace("Get ", "")

        except AttributeError:
            get_text = tdiv.find_all(
                "a", {"class": "wallet-info"})[1].text
            earn = get_text.replace("Get ", "")
        return earn

    tdivs = soup.find_all(
        "div", {"class": "vault my-1 p-2 bg-white wallet-empty vault-empty wallet-farm-empty farm-empty farm-rewards-empty"})

    site_data = {}
    for tdiv in tdivs:

        coin = tdiv.find("div", {
            "class": "col-sm col-12"}).text.strip()

        if coin.find("-") != -1 or coin in IGNORE:
            pass

        else:
            apy = tdiv.find("div", {
                "class": "col-sm col-12 text-center"}).find("span", {"class": "text-primary"}).text

            earn_perc = ("apy", apy)
            earn = get_earn(tdiv)

            update_data(site_data, coin, earn, earn_perc,
                        name, url, tag)

    return site_data


def gecko(soup, name, url):
    return viking(soup, name, url)


# @retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def cream(soup, name, url, tag, earn_type="apy", IGNORE=[]):

    t_tdiv = soup.find_all(
        "div", {"class": "sc-dJjZJu cRWJtq rdt_TableBody"})

    tdivs = t_tdiv[0].find_all(
        "div", {"class": "sc-jrQzUz kKwhjt rdt_TableRow"})

    site_data = {}
    for tdiv in tdivs:

        coin = tdiv.find("div", {
            "class": "sc-hKwCoD sc-eCImvq sc-jRQAMF iFTwCY gTuvxR fdclGF rdt_TableCell"}).text

        apy = tdiv.find("div", {
            "class": "sc-hKwCoD sc-eCImvq sc-jRQAMF iFTwCY kOQSBM eIKzDm rdt_TableCell"}).text

        earn = coin

        if coin.find("-") != -1 or coin in IGNORE:
            pass
        else:

            earn_perc = (earn_type, apy)
            update_data(site_data, coin, earn, earn_perc,
                        name, url, tag)

    return site_data


funcs = {
    "acryptos": acryptos,
    "auto": auto,
    "jetfuel": jetfuel,
    "beefy": beefy,
    "pancakebunny": bunny,
    "vikingswap": viking,
    "cream": cream
}


@retry(exceptions=Exception, tries=3, delay=60*3, max_delay=None, backoff=60*2)
def scrape_sites(params_path=None, sites_path=None, images_path=None, _export=False, prod=False):
    DATA = {}
    data = {}

    def export(_data):
        with open("data.json", "w") as fout:
            json.dump(_data, fout)

    if params_path == None:
        params_path = "params.yaml"
    if sites_path == None:
        sites_path = "sites.json"

    with open(sites_path) as f:
        SITES = json.load(f)
    with open(params_path) as f:
        params = yaml.load(f, Loader=yaml.FullLoader)
        ACTIVE_SITES = params["active_sites"]
        SLEEP = params["sleep"]

    for site in SITES:
        page_source = None
        data = None
        if site["tag"] in ACTIVE_SITES and site["code"] == 1:
            logger.info("Scraping data for site: {}".format(site["tag"]))
            driver = webdriver.Firefox(
                executable_path=os.path.abspath("geckodriver"))
            URL = site["urls"]
            driver.get(URL)
            time.sleep(SLEEP)
            page_source = driver.page_source
            driver.quit()

        elif site["tag"] in ACTIVE_SITES and site["tag"] == "cream":
            logger.info("Scraping data for site: {}".format(site["tag"]))
            driver = webdriver.Firefox(
                executable_path=os.path.abspath("geckodriver"))
            URL = site["urls"]
            driver.get(URL)

            wait = WebDriverWait(driver, 20)
            actions = ActionChains(driver)

            e = driver.find_element(By.XPATH, '//span[text()="Ethereum"]')
            actions.move_to_element(e).perform()

            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//li[text()="BSC"]'))).click()

            wait.until(EC.visibility_of_element_located(
                (By.XPATH, '//div[text()="Show more"]'))).click()

            time.sleep(SLEEP)
            page_source = driver.page_source
            driver.quit()

        elif site["tag"] in ACTIVE_SITES and site["tag"] == "beefy":

            data = funcs[site["tag"]](site["name"], site["urls"], site["tag"])

            if bool(data) == False:
                logger.warning("NO DATA...sending email")
                if prod == True:
                    m.email("{} return empty data".format(site["tag"]))

        if page_source:
            soup = BeautifulSoup(page_source, 'lxml')

            data = funcs[site["tag"]](soup, site["name"], URL, site["tag"])

            if bool(data) == False:
                logger.warning("NO DATA...sending email")
                if prod == True:
                    m.email("{} return empty data".format(site["tag"]))

        if data:
            DATA[site["tag"]] = data

    if _export == True:
        export(DATA)
        logger.info("Data exported...")


if __name__ == "__main__":

    scrape_sites(_export=False)
