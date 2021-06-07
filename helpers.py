from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import smtplib
import json


def find(n, tokens):
    for token in tokens:
        if n.find(token) != -1:
            return token


def replace(n, tokens):
    for token in tokens:
        if n.find(token.lower()) != -1:
            n = n.replace(token.lower(), token)
            return n


def scroll_down_all(driver):
    SCROLL_PAUSE_TIME = 0.5

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


class Message:

    def __init__(self):
        with open("../config.json") as f:
            conf = json.load(f)
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login("dav.lanigan@gmail.com", conf["gmail"]["password"])

    def email(self, msg):
        e = "dav.lanigan@gmail.com"
        message = "Subject: {}\n\n {}".format("se ERROR MSG", msg)
        self.server.sendmail(e, e, message)


if __name__ == "__main__":

    m = Message()
    m.email("Hey there.")
