import logging
import secrets
from datetime import datetime
from typing import Optional

import databases
from asyncpg import UniqueViolationError
from dicttoxml import dicttoxml
from faker import Faker
from fastapi import (
    FastAPI,
    status,
    Header,
    Response,
    Request,
    Depends,
    HTTPException,
    Query
)
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select, insert
from starlette.responses import RedirectResponse

from config import config
from models import (
    UsersResponse,
    UserResponse,
    UserCreateRequest,
    Users,
    Book,
    Books,
    LinkBooksForUser,
)

database = databases.Database(config.db_url)

app = FastAPI()

log = logging.getLogger('API')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)
log.setLevel(logging.INFO)

security = HTTPBasic()


class UnicornException(Exception):
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    # correct_username = secrets.compare_digest(credentials.username, "stanleyjobson")
    correct_password = secrets.compare_digest(credentials.password, "Test123#")
    log.info('Auth: %s ,%s', correct_password, credentials)
    if not (credentials.username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def convert_to_xml(model):
    if getattr(model, '__root__', None):
        model = [m.dict() for m in model.__root__]
    else:
        model = model.dict()
    return dicttoxml(model, custom_root=model.__class__.__name__, attr_type=False)


def _response(result, type_='application/json'):
    log.debug('result: %s', result)
    if type_ == 'application/xml':
        return Response(content=convert_to_xml(result), media_type=type_)
    return result


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! Для поля {exc.name} не уникальное значение: {exc.value}"},
    )


@app.get('/')
async def docs():
    return RedirectResponse(url='/docs')


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


@app.get("/users", response_model=UsersResponse)
async def read_root(
        offset: int = 0,
        limit: int = Query(default=10, lte=50),
        content_type: Optional[str] = Header(None)
):
    users = UsersResponse.parse_obj(
        await database.fetch_all(select(Users).offset(offset).limit(limit))
    )
    return _response(users, content_type)


@app.get('/users/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, content_type: Optional[str] = Header(None)):
    return _response(
        UserResponse(
            **(await database.fetch_one(
                select(Users).where(Users.id == user_id)
            ))
        ),
        content_type
    )


@app.post('/users', response_model=UserResponse)
async def create_user(user: UserCreateRequest, username: str = Depends(get_current_username)):
    try:
        result = await database.fetch_one(
            insert(Users).values(
                name=user.name,
                email=user.email,
                created_by=username,
                created_at=datetime.now()
            ).returning(*Users.__table__.c.values())
        )
    except UniqueViolationError:
        raise UnicornException('email', user.email)
    log.debug(list(result.values()))
    return UserResponse.parse_obj(result)


@app.get('/users/{user_id}/books', response_model=Books)
async def get_user_books(user_id: int, content_type: Optional[str] = Header(None)):
    pass


@app.get('users/users/{user_id}/books/{book_id}', response_model=Book)
async def get_user_book(self, user_id: int, book_id: int, content_type: Optional[str] = Header(None)):
    pass


@app.post('/users/{user_id}/books/{book_id}', response_model=Book)
async def add_book_touser(
        user_id: int,
        book_id: int,
        books_with_users: LinkBooksForUser,
        username: str = Depends(get_current_username)
):
    pass
