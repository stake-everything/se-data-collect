import json
import pyrebase

print("working...")
with open("../config.json") as f:
    config = json.load(f)

with open("sites.json") as f:
    SITES = json.load(f)


firebase = pyrebase.initialize_app(config['firebase'])
db = firebase.database()


db.update({"sites": SITES})


print("done...")
