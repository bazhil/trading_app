from fastapi import FastAPI


app = FastAPI(
    title='Trading app'
)

fake_users = [
    {'id': 1, 'name': 'Bob'},
    {'id': 2, 'name': 'John'}
]

@app.get('/users/{id}')
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
