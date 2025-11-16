from fastapi import FastAPI
app = FastAPI()

from sqlalchemy.orm import Session
from . import schemas
from webapp_db import user_table

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_item(db: Session, user: schemas.UserCreate):
    db_item = models.User(name=user.username, description=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#get all users


#create new user
@app.post("/add_user/")
def

#adjust user username


#delete user


