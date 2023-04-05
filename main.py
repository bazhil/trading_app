from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def hello():
    return {'Message': 'Welcome to the trading app'}


