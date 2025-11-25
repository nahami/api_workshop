from fastapi import FastAPI
from webapp_db import select_user
from webapp_db import *
import pandas as pd 
from sqlalchemy import select, update

app = FastAPI()

engine = sa.create_engine("sqlite:///webapp_database.db", echo = True)
connection = engine.connect()

#get all users
@app.get("/getusers")
def get_users():
    data = select_user()
    data_df = pd.DataFrame.from_records(data = data,
                                    index='user_table__id',
                                    columns=['user_table__id', 'username','email'])
    print(data_df[['username','email']])
    return data_df[['username','email']]
    # return data_df['username']

#insert new user
@app.post("/add_user")
def add_user(username: str, email: str):
    insert_user(username=username, email=email)
    connection.commit()
    connection.close()
    return "user added" 
    # return data_df['username']



#adjust emailadres 
@app.put("/change_email/{id}")
def change_email(id: int, new_email: str):
    result = connection.execute(select(user_table).where(user_table.c.id == id)).fetchone()
    
    if not result:
        return {"error": "User not found"}

    # Update email
    upd = (
        update(user_table)
        .where(user_table.c.id == id)
        .values(email=new_email)
    )
    connection.execute(upd)
    connection.commit()
    # connection.close()
    return "user email updated" 
    # return data_df['username']
    
#delete user
@app.delete("/delete_user/{id}")
def delete_user(id: int):
    result = connection.execute(select(user_table).where(user_table.c.id == id)).fetchone()
    
    if not result:
        return {"error": "User not found"}

    # Delete user
    del_stmt = user_table.delete().where(user_table.c.id == id)
    connection.execute(del_stmt)
    connection.commit()
    return "user deleted"    
    

# test in http://127.0.0.1:8000/docs#/

