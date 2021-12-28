import csv
import io
import logging
import secrets
from datetime import datetime
from enum import Enum
from typing import Union, Any, Dict

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
    Query,
)
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import select, insert

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
from swagger import tags, users_responses

database = databases.Database(config.db_url)

app = FastAPI(openapi_tags=tags)

log = logging.getLogger('API')
stream = logging.StreamHandler()
stream.setLevel(logging.INFO)
log.addHandler(stream)
log.setLevel(logging.INFO)

security = HTTPBasic()


class Types(str, Enum):
    json = 'application/json'
    xml = 'application/xml'


class UserTypes(str, Enum):
    json = 'application/json'
    xml = 'application/xml'
    csv = 'text/csv'


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


def convert_to_xml(model, custom_root=''):
    if getattr(model, '__root__', None):
        model = [m.dict() for m in model.__root__]
    else:
        model = model.dict()
    return dicttoxml(
        model,
        custom_root=custom_root or model.__class__.__name__,
        attr_type=True,
        # ids=True
    )


def _response(result, type_: UserTypes = Types.json, custom_root=''):
    log.debug('result: %s', result)
    if type_ == Types.xml:
        return Response(content=convert_to_xml(result, custom_root=custom_root), media_type=type_)
    if type_ == UserTypes.csv:
        result = [m.dict() for m in result.__root__]
        file = io.StringIO()
        dict_writer = csv.DictWriter(file, result[0].keys(), dialect='excel')
        dict_writer.writeheader()
        dict_writer.writerows(result)

        response = StreamingResponse(iter([file.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=export.csv"
        return response

    return result


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=400,
        content={"message": f"Oops! Для поля {exc.name} не уникальное значение: {exc.value}"},
    )


@app.get('/', include_in_schema=False)
async def docs():
    return RedirectResponse(url='/docs')


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get('/new_users', include_in_schema=False, tags=['User'])
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


@app.get(
    "/users",
    response_model=Union[UsersResponse, Dict[str, Any], str],
    tags=['User'],
    responses=users_responses
)
async def read_root(
        offset: int = 0,
        limit: int = Query(default=10, lte=50),
        accept: UserTypes = Header(UserTypes.json)
):
    users = UsersResponse.parse_obj(
        await database.fetch_all(select(Users).offset(offset).limit(limit))
    )
    return _response(users, accept, custom_root='Users')


@app.get('/users/{user_id}', response_model=UserResponse, tags=['User'])
async def get_user(user_id: int, accept: Types = Header(Types.json)):
    return _response(
        UserResponse(
            **(await database.fetch_one(
                select(Users).where(Users.id == user_id)
            ))
        ),
        accept
    )


@app.post('/users', response_model=Union[UserResponse], tags=['User'])
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


@app.get('/users/{user_id}/books', response_model=Books, tags=['Books'])
async def get_user_books(
        user_id: int,
        accept: Types = Header(Types.json)):
    pass


@app.get('users/users/{user_id}/books/{book_id}', response_model=Book, tags=['Books'])
async def get_user_book(
        user_id: int,
        book_id: int,
        accept: Types = Header(Types.json)
):
    pass


@app.post('/users/{user_id}/books/{book_id}', response_model=Book, tags=['Books'])
async def add_book_touser(
        user_id: int,
        book_id: int,
        books_with_users: LinkBooksForUser,
        username: str = Depends(get_current_username)
):
    pass
