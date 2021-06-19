# key - value
# key is user's discord userid
# value is a list with username, questions attempted, questions solved, questions posted, 0, 0, 0, "", "", ""

from replit import db

def clear_database():
  keys = db.keys()
  for key in keys:
    print(key, db[key])
    del db[key]

clear_database()