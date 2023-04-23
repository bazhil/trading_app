from datetime import datetime
from enum import Enum
from typing import List, Optional

from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel, Field

from fastapi import FastAPI

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.database import User

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title='Trading app'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


fake_users = [
    {'id': 1, 'name': 'Bob', 'degree': [
        {'id': 1, 'created_at': '2020-01-01T00:00:00', 'type_degree': 'expert'}
    ]},
    {'id': 2, 'name': 'John'}
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get('/users/{id}', response_model=List[User])
def get_user(id: int):
    return [user for user in fake_users if user.get('id') == id]


fake_trades = [
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'buy', 'price': 123, 'amount': 2.12},
    {'id': 1, 'user_id': 1, 'currency': 'BTC', 'side': 'sell', 'price': 125, 'amount': 2.12}
]

@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    current_user = [user for user in fake_users if user.get('id') == user_id]
    if not current_user:
        return {'status': 404, 'message': 'User does not exists'}

    current_user[0]['name'] = new_name

    return {'status': 200, 'data': current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=20)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def post_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}
