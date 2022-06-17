from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = []

class City(BaseModel):
    name: str
    timezone: dict

@app.get('/')
def index():
    return  {'key': 'value'}

@app.get('/cities')
def get_cities():
    return db

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]
