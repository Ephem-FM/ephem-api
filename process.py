import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def main(preferences = None):
    df = retrieve_df('playlists')
    # preferences = {
    #     'artist popularity': 25,
    #     'danceability': .61,
    #     'valence': .70,
    #     'energy': .61
    # }
    return top_three_shows(df, preferences)

def retrieve_df(table_name):
    # enter in characteristics of different databases
    DATABASES = {
        'production':{
            'NAME': 'dc3j53nnljkf17',
            'USER': 'qckrwbcldmcbua',
            'PASSWORD': 'd843c6fcbe8d0411c1f113f00fdc458459f530b6bbf629a7c15e25ad09bf23e7',
            'HOST': 'ec2-3-226-163-72.compute-1.amazonaws.com',
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
    print(gf)
    # gets difference between a user's preferences and a show's mean
    def get_score(num1, num2):
        return (1 - abs(num1-num2))

    # a dict of show names and composite score
    shows_composite = {}
    for row in gf.itertuples():
        print(row)
        composite_score = get_score(preferences['artist popularity']/100, row[1]/100) + get_score(preferences['danceability'], row[2]) + get_score(preferences['valence'], row[3]) + get_score(preferences['energy'], row[5])
        shows_composite[row[0]] = composite_score

    # retrieve top 3 shows based on composite score
    series = pd.Series(shows_composite)
    top_3 = series.sort_values(ascending=False)[0:3]
    return top_3

if __name__=="__main__":
    print(main())
