from fastapi import FastAPI
from pydantic import BaseModel

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
    return "hi friend"
    # db[-1]

