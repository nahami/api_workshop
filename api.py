from fastapi import FastAPI, Request, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from webapp_db import select_user
from webapp_db import *
import pandas as pd 
from sqlalchemy import select, update
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

FAKE_USER = {
    "username": "admin",
    "password": "password123"
}

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

app = FastAPI()

engine = sa.create_engine("sqlite:///webapp_database.db", echo = True)
connection = engine.connect()

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    if username != FAKE_USER["username"] or password != FAKE_USER["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token(
        data={"sub": username, "type": "access"},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    refresh_token = create_token(
        data={"sub": username, "type": "refresh"},
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")

        if username is None or token_type != "access":
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@app.post("/refresh")
def refresh_token(refresh_token: str = Form(...)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_token(
            data={"sub": username, "type": "access"},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@app.get("/getusers")
def get_users():
    data = select_user()
    data_df = pd.DataFrame.from_records(data = data,
                                    # index='user_table__id',
                                    columns=['user_table__id','username','email']
                                    )
    # print(data_df[['username','email']])
    print(data_df)
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

@app.post("/add-user")
async def add_user2(request: Request):
    data = await request.json()

    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        raise HTTPException(status_code=400, detail="username and email are required")

    insert_user(username=username, email=email)
    connection.commit()
    connection.close()

    return {"message": "user added"}

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
# test in http://127.0.0.1:8000/docs#/

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