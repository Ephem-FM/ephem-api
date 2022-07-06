from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

db = []

class Preferences(BaseModel):
    valence: float
    energy: float
    popularity: int

# @app.get('/')
# def index():
#     return  {'key': 'value'}

# @app.get('/cities')
# def get_cities():
#     return db

@app.post('/preferences')
def create_city(preferences: Preferences):
    db.append(preferences.dict())
    return db[-1]

