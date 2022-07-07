from fastapi import FastAPI
from pydantic import BaseModel
import process

app = FastAPI()

db = []

class Preferences(BaseModel):
    valence: float
    energy: float
    danceability: float
    popularity: float

# @app.get('/')
# def index():
#     return  {'key': 'value'}

# @app.get('/preferences')
# def get_cities():
#     return db

@app.post('/preferences')
def create_recs(preferences: Preferences):
    db.append(preferences.dict())
    top_3 = process.main(preferences.dict())
    return top_3

