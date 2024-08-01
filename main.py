from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
from datetime import datetime

app = FastAPI()

USERS_FILE = 'users.json'

# Структура данных пользователя
class User(BaseModel):
    name: str
    phone: str

class UserInDB(User):
    id: int
    date_added: str

# Функция для чтения данных пользователей из файла
def read_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r') as file:
        return json.load(file)

# Функция для записи данных пользователей в файл
def write_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# GET метод для получения информации о пользователе по ID
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    users = read_users()
    user = next((user for user in users if user["id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# POST метод для добавления нового пользователя
@app.post("/user", response_model=UserInDB)
async def create_user(user: User):
    users = read_users()
    if users:
        new_id = max(user["id"] for user in users) + 1
    else:
        new_id = 1
    new_user = UserInDB(
        id=new_id,
        name=user.name,
        phone=user.phone,
        date_added=datetime.now().isoformat()
    )
    users.append(new_user.dict())
    write_users(users)
    return new_user
