from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import uvicorn


class User(BaseModel):
    id: Optional[int] = None
    username: str
    wallet: float
    birthdate: date


class UserUpdate(BaseModel):
    username: Optional[str] = None
    wallet: Optional[float] = None
    birthdate: Optional[date] = None


app = FastAPI()

db_users = [
    User(id=1, username="user1", wallet=100.0, birthdate=date(1990, 1, 1)),
    User(id=2, username="user2", wallet=200.0, birthdate=date(1995, 5, 15)),
]


# Получение списка всех пользователей
@app.get("/users/", response_model=List[User])
async def read_users():
    return db_users


# Получение пользователя по его ID
@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Создание пользователя
@app.post("/users/", response_model=User)
async def create_user(user: User):
    next_id = max([user.id for user in db_users]) + 1
    user.id = next_id
    db_users.append(user)
    return user


# Обновление данных пользователя по id
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, update: UserUpdate):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for attr_name, attr_value in update.dict().items():
        if attr_value is not None:
            setattr(user, attr_name, attr_value)

    return user


# Удаление пользователя по его ID.
@app.delete("/users/{user_id}")
async def update_user(user_id: int):
    user = next((user for user in db_users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_users.remove(user)
    return {"Ответ": "Пользователь удален"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
