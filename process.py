import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def main(preferences = None):
    df = retrieve_df('playlists')
    top_three = top_three_shows(df, preferences)
    shows = retrieve_show_info(top_three.keys())
    return shows
    
def retrieve_df(table_name):
    # enter in characteristics of different databases
    DATABASES = {
        'production':{
            'NAME': NAME,
            'USER': USER,
            'PASSWORD': PW,
            'HOST': HOST,
            'PORT': 5432,
        },
    }

    # choose the database to use
    db = DATABASES['production']

    # construct an engine connection string
    engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
        user = db['USER'],
        password = db['PASSWORD'],
        host = db['HOST'],
        port = db['PORT'],
        database = db['NAME'],
    )

    # create sqlalchemy engine
    engine = create_engine(engine_string)

    # read a table from database into pandas dataframe, replace "tablename" with your table name
    return pd.read_sql_table(table_name, engine)

def top_three_shows(df, preferences):
    gf = df.groupby('show_id').mean()
    pd.set_option("display.max_rows", None)
    # gets difference between a user's preferences and a show's mean
    def get_score(num1, num2):
        return (1 - abs(num1-num2))

    # a dict of show names and composite score
    shows_composite = {}
    for row in gf.itertuples():
        composite_score = get_score(preferences['popularity']/100, row[1]/100) + get_score(preferences['danceability'], row[2]) + get_score(preferences['valence'], row[3]) + get_score(preferences['energy'], row[5])
        shows_composite[row[0]] = composite_score

    # retrieve top 3 shows based on composite score
    series = pd.Series(shows_composite)
    top_3 = series.sort_values(ascending=False)[0:3]
    return top_3

def retrieve_show_info(show_ids):
    conn = psycopg2.connect(CONNECTION_STRING)
    conn.autocommit = True
    cur = conn.cursor()
    shows = []
    # get info for each show from 'showverviews' table based on id
    for show_id in show_ids:
        select_q = """ SELECT * FROM showverviews WHERE id=%s """
        select_t = (show_id,)
        cur.execute(select_q, select_t)
        shows.append(cur.fetchone())
    conn.commit()
    cur.close()
    return shows

if __name__=="__main__":
    print(main())
