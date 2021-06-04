from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
import time
import json
import os

os.environ['MOZ_HEADLESS'] = '1'


def update_data(site_data, coin, earn, earn_perc, name, url):

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
    }
    site_data[coin][earn_perc[0]] = parse_perc(earn_perc[1])


def auto(soup, name, url):
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
            coin = coin.replace("belt", "").replace("i", "")

            # get earn and earn_perc (%)
            earn = tdiv.find(earn_el["type"], {
                             "class": earn_el["class"]}).find_all("div")[0].text
            earn_perc = tdiv.find(
                perc_el["type"], {"class": perc_el["class"]}).text

            update_data(site_data, coin, earn,
                        (EARN_TYPE, earn_perc), name, url)

    return site_data


def jetfuel(soup, name, url):
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
                        name, url)

    return site_data


def beefy(self):
    driver = webdriver.Firefox()
    for site in self.SITES:
        if site["type"] == "beefy":
            URL = site["urls"]
            driver.get(URL)
            time.sleep(15)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'lxml')

            print(soup.prettify())

            tdivs = soup.find_all(
                "div", {"class": "MuiGrid-root jss1564 MuiGrid-container MuiGrid-item MuiGrid-grid-xs-12since"})

            print(tdivs[0])

            # coin = tdivs[0]

            driver.quit()

            site_data = {}
            for tdiv in tdivs:

                coin = tdiv.find(
                    "div", {"class": "label"}).find_all("span")[0].text
                apy = tdiv.find(
                    "div", {"class": "rates"}).find_all("span")[0].text
                earn = tdiv.find("div", {"class": "details return"}).find_all(
                    "span", {"class": "value"})[0].text

                coin.replace("belt", "").replace("i", "")

                if coin.find("-") == -1:

                    d = {
                        "stake": coin,
                        "earn": earn,
                        "apr": None,
                        "apy": apy,
                        "name": site["name"],
                        "url": URL
                    }
                    site_data[coin] = d

            if bool(site_data) != False:
                self.DATA[site["name"]] = site_data
    driver.quit()


def bunny(soup, name, url):
    IGNORE = []
    EARN_TYPE = "apy"

    tdivs = soup.find_all("div", {"class": "row"})

    print(tdivs)

    site_data = {}
    for tdiv in tdivs[1:]:

        coin = tdiv.find(
            "div", {"class": "label"}).find_all("span")[0].text

        print(coin)

        if coin.find("-") != -1 or coin in IGNORE:
            pass
        else:

            apy = tdiv.find(
                "div", {"class": "rates"}).find_all("span")[0].text
            earn_perc = (EARN_TYPE, apy)

            earn = tdiv.find("div", {"class": "details return"}).find_all(
                "span", {"class": "value"})[0].text

            update_data(site_data, coin, earn, earn_perc,
                        name, url)

    return site_data


def viking(soup, name, url):
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

            update_data(site_data, coin, earn, earn_perc, name, url)

    return site_data


def acryptos(soup, name, url):
    IGNORE = ["A2B2", "ACS3", 'ACS3BTC', 'ACS4USD', 'ACS4VAI', 'ACS4UST']

    def get_earn(tdiv):
        try:
            get_text = tdiv.find_all(
                "a", {"class": "wallet-info"})[1].text
            earn = get_text.replace("Get ", "")
        except AttributeError:
            get_text = tdiv.find("span", {"class": "wallet-info"}).text
            get_text = get_text[:get_text.find(":")]
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
                        name, url)

    return site_data


def gecko(soup, name, url):
    return viking(soup, name, url)


funcs = {
    "acryptos": acryptos,
    "auto": auto,
    "jetfuel": jetfuel,
    "beefy": beefy,
    "pancakebunny": bunny,
    "vikingswap": viking
}


def scrape_sites(params_path=None, sites_path=None, images_path=None, _export=False):
    DATA = {}

    def export(_data):
        with open("data.json", "w") as fout:
            json.dump(_data, fout)

    if params_path == None:
        params_path = "params.json"
    if sites_path == None:
        sites_path = "sites.json"

    with open(sites_path) as f:
        SITES = json.load(f)
    with open(params_path) as f:
        params = json.load(f)
        ACTIVE_SITES = params["active_sites"]
        SLEEP = params["sleep"]

    for site in SITES:
        if site["tag"] in ACTIVE_SITES:
            print(site["tag"])
            driver = webdriver.Firefox()
            URL = site["urls"]
            driver.get(URL)
            time.sleep(SLEEP)
            page_source = driver.page_source
            driver.quit()

            soup = BeautifulSoup(page_source, 'lxml')

            data = funcs[site["tag"]](soup, site["name"], URL)

            print(data)
            DATA[site["tag"]] = data

    if _export == True:
        print(DATA)
        export(DATA)


if __name__ == "__main__":

    scrape_sites(_export=True)


"""------------------------"""


# def goose(soup, name, url):
#     IGNORE = []
#     EARN_TYPE = "apr"

#     tdivs = soup.find_all("div", {"class": "sc-ikPAkQ diwHUn"})
#     site_data = {}
#     for tdiv in tdivs:
#         ldivs = tdiv.find_all("div", {"class": "sc-gsTCUz UNsmv"})

#         apr = ldivs[0].text
#         earn_perc = (EARN_TYPE, apr)
#         coin = ldivs[1].text
#         earn = ldivs[2].text

#         update_data(site_data, coin, earn, earn_perc,
#                     name, url)
#     return site_data

"""
        "jetfuel",
        "acryptos",
        "auto",
        "vikingswap"
"""
