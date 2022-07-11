import string
from fastapi import FastAPI
from pydantic import BaseModel
import process

app = FastAPI()

db = []

class Preferences(BaseModel):
    phone: str
    valence: float
    energy: float
    danceability: float
    popularity: int

# @app.get('/')
# def index():
#     return  {'key': 'value'}

# @app.get('/preferences')
# def get_cities():
#     return db

@app.post('/preferences')
def create_recs(preferences: Preferences):
    print("PREFERENCES: ", preferences)
    return process.main(preferences.dict())

if __name__=="__main__":
    preferences = {
        'phone': '5127759300',
        'artist popularity': 64,
        'danceability': .24,
        'valence': .70,
        'energy': .5
    }
    print(process.main(preferences))

