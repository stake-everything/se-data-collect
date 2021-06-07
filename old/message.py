import smtplib
import json


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
