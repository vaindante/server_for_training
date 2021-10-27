import logging
from datetime import datetime

import databases
from faker import Faker
from fastapi import FastAPI, status
from sqlalchemy import select, insert
from fastapi.responses import JSONResponse
from config import config
from models import (
    UsersResponse,
    UserResponse,
    UserCreateRequest,
    Users,
)

database = databases.Database(config.db_url)

app = FastAPI()

log = logging.getLogger('API')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)
log.setLevel(logging.INFO)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/new_users')
async def new_users():
    faker = Faker(locale='ru-Ru')
    values = [
        {
            'email': faker.email(),
            'name': faker.name(),
            'created_at': faker.date_between(start_date='-1y'),
            'created_by': 1,
        }
        for _ in range(5)
    ]
    try:
        await database.execute_many(insert(Users), values=values)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'status': True})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={'error': e.__name__})


@app.get("/", response_model=UsersResponse)
async def read_root():
    users = await database.fetch_all(select(Users))
    return UsersResponse.parse_obj(users)


@app.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int):
    return UserResponse(
        **(await database.fetch_one(
            select(Users).where(Users.id == user_id)
        ))
    )


@app.post('/', response_model=UserResponse)
async def create_user(user: UserCreateRequest):
    result = await database.fetch_one(
        insert(Users).values(
            name=user.name,
            email=user.email,
            created_by=1,
            created_at=datetime.now()
        ).returning(*Users.__table__.c.values())
    )
    log.info(list(result.values()))
    return UserResponse.parse_obj(result)
