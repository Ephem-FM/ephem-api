import string
from fastapi import FastAPI
from pydantic import BaseModel
import process

app = FastAPI()

class Preferences(BaseModel):
    phone: str
    valence: float
    energy: float
    danceability: float
    popularity: int

@app.post('/preferences')
def create_recs(preferences: Preferences):
    print("PREFERENCES: ", preferences)
    shows = process.main(preferences.dict())
    print("shows", shows)
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
