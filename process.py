import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def main():
    df = retrieve_df('playlists')
    top_three_shows(df)
   

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

def top_three_shows(df):
    gf = df.groupby('show').mean()
    pd.set_option("display.max_rows", None)
    # print(gf)
    for row in gf.itertuples():
        print("show: ", row[0])
        print("artist popularity: ", row[1])
        print("danceability: ", row[2])
        print("valence: ", row[3])
        print("energy: ", row[4])
        print()

if __name__=="__main__":
    main()