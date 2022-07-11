import string
from fastapi import FastAPI
from numpy import number
from pydantic import BaseModel
import process
import texts

app = FastAPI()

class Preferences(BaseModel):
    phone: str
    valence: float
    energy: float
    danceability: float
    popularity: int

@app.post('/preferences')
def create_recs(preferences: Preferences):
    preferences = preferences.dict()
    shows = process.main(preferences)
    texts.send_introductory_text(preferences['phone'])
    for s in shows:
        texts.main(preferences['phone'], s)
    return shows

if __name__=="__main__":
    preferences = {
        'phone': '5127759300',
        'artist popularity': 64,
        'danceability': .24,
        'valence': .70,
        'energy': .5
    }
    print(process.main(preferences))


# @app.get('/')
# def index():
#     return  {'key': 'value'}

# @app.get('/preferences')
# def get_cities():
#     return db
