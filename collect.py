from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
import time
import json
import os

os.environ['MOZ_HEADLESS'] = '1'


class Scrape:

    def __init__(self, path=None):
        if path == None:
            path = "sites.json"

        with open(path) as f:
            self.SITES = json.load(f)

        self.DATA = {}
        self.SLEEP = 5

    def export(self):
        with open("data.json", "w+") as fout:
            json.dump(self.DATA, fout)

    def auto(self):
        driver = webdriver.Firefox()
        for site in self.SITES:
            if site["type"] == "auto":
                URL = site["urls"]
                driver.get(URL)
                time.sleep(self.SLEEP)

                page_source = driver.page_source

                soup = BeautifulSoup(page_source, 'lxml')

                tdivs = soup.find_all(
                    "div", {"class": "text-left text-sm sm:text-base py-2"})

                site_data = {}
                for tdiv in tdivs:

                    coin = tdiv.find(
                        "div", {"class": "font-semibold flex space-x-2"}).find_all("div")[0].text

                    earn = tdiv.find("div", {
                        "class": "grid grid-rows-2 items-center text-gray-500 dark:text-gray-400 font-semibold text-xs sm:text-sm"}).find_all("div")[0].text

                    earn = earn.replace("Farm:\xa0", "")

                    apy = tdiv.find(
                        "div", {"class": "text-sm sm:text-base"}).text

                    if coin.find("-") == -1:
                        d = {
                            "stake": coin,
                            "earn": earn,
                            "apr": None,
                            "apy": apy,
                            "name": site["name"],
                            "url": URL
                        }

                        coin = coin.replace("belt", "").replace("i", "")
                        site_data[coin] = d

                if bool(site_data) != False:
                    self.DATA[site["name"]] = site_data
        driver.quit()

    def acryptos(self):
        driver = webdriver.Firefox()
        for site in self.SITES:
            if site["type"] == "acryptos":
                URL = site["urls"]
                driver.get(URL)
                time.sleep(15)

                page_source = driver.page_source

                soup = BeautifulSoup(page_source, 'lxml')

                tdivs = soup.find_all(
                    "div", {"class": "vault my-1 p-2 bg-white wallet-empty vault-empty wallet-farm-empty farm-empty farm-rewards-empty"})

                site_data = {}
                for tdiv in tdivs:

                    coin = tdiv.find("div", {
                        "class": "col-sm col-12"}).text.strip()
                    apy = tdiv.find("div", {
                        "class": "col-sm col-12 text-center"}).find("span", {"class": "text-primary"}).text

                    get_text = tdiv.find("span", {"class": "wallet-info"}).text
                    get_text = get_text[:get_text.find(":")]
                    earn = get_text.replace("Get ", "")

                    if coin.find("-") == -1:
                        site_data[coin] = {
                            "stake": coin,
                            "earn": earn,
                            "apr": None,
                            "apy": apy,
                            "name": site["name"],
                            "url": URL
                        }

                if bool(site_data) != False:
                    self.DATA[site["name"]] = site_data
        driver.quit()

    def beefy(self):
        driver = webdriver.Firefox()
        for site in self.SITES:
            if site["type"] == "beefy":
                URL = site["urls"]
                driver.get(URL)
                time.sleep(self.SLEEP)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                tdivs = soup.find_all("div", {"class": "row"})

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

    def bunny(self):
        driver = webdriver.Firefox()
        for site in self.SITES:
            if site["type"] == "bunny":
                URL = site["urls"]
                driver.get(URL)
                time.sleep(self.SLEEP)

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                tdivs = soup.find_all("div", {"class": "row"})

                site_data = {}
                for tdiv in tdivs:

                    coin = tdiv.find(
                        "div", {"class": "label"}).find_all("span")[0].text
                    apy = tdiv.find(
                        "div", {"class": "rates"}).find_all("span")[0].text
                    earn = tdiv.find("div", {"class": "details return"}).find_all(
                        "span", {"class": "value"})[0].text

                    if coin.find("-") == -1:
                        site_data[coin] = {
                            "stake": coin,
                            "earn": earn,
                            "apr": None,
                            "apy": apy,
                            "name": site["name"],
                            "url": URL
                        }

                if bool(site_data) != False:
                    self.DATA[site["name"]] = site_data
        driver.quit()

    def goose(self):
        driver = webdriver.Firefox()

        for site in self.SITES:
            if site["type"] == "goose":
                URL = site["urls"]
                driver.get(URL)
                time.sleep(self.SLEEP)
                page_source = driver.page_source

                soup = BeautifulSoup(page_source, 'lxml')

                tdivs = soup.find_all("div", {"class": "sc-ikPAkQ diwHUn"})
                site_data = {}
                for tdiv in tdivs:
                    ldivs = tdiv.find_all("div", {"class": "sc-gsTCUz UNsmv"})

                    apr = ldivs[0].text
                    coin = ldivs[1].text
                    earn = ldivs[2].text

                    site_data[coin] = {
                        "stake": coin,
                        "earn": earn,
                        "apr": apr,
                        "apy": None,
                        "name": site["name"],
                        "url": URL
                    }

                self.DATA[site["name"]] = site_data

        driver.quit()

    def viking(self):
        driver = webdriver.Firefox()
        for site in self.SITES:
            if site["type"] == "viking":
                URL = site["urls"]
                driver.get(URL)
                time.sleep(self.SLEEP)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'lxml')
                tdivs = soup.find_all("div", site["tdiv"])
                site_data = {}
                for tdiv in tdivs:

                    coin = tdiv.find_all("h2")[0].text
                    ldivs = tdiv.find_all("div", {"class": site["ldiv"]})

                    apr = ldivs[0].text
                    earn = ldivs[1].text

                    site_data[coin] = {
                        "stake": coin,
                        "earn": earn,
                        "apr": apr,
                        "apy": None,
                        "name": site["name"],
                        "url": URL
                    }
                self.DATA[site["tag"]] = site_data
        driver.quit()


if __name__ == "__main__":

    s = Scrape()
    # s.bunny()
    # s.auto()
    # s.acryptos()
    # s.viking()
    # s.export()
    # print(s.DATA)
