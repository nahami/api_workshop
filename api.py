from fastapi import FastAPI
from webapp_db import select_user
from webapp_db import *

app = FastAPI()

engine = sa.create_engine("sqlite:///webapp_database.db", echo = True)
connection = engine.connect()

#get all users
@app.get("/getusers")
def get_users():
    data = select_user(username='Arjan')
    print("test")
    resultaat = ''
    for record in data:
        resultaat += record[1] + "end=/n"        
        print("tussenresultaat= ",resultaat)
    return resultaat

