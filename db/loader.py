import sqlalchemy as sa
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    url = "postgresql+psycopg2://postgres:realestate123@localhost:5432/realestate"
    return sa.create_engine(url)
    
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return sa.create_engine(url)

def load_dataframe(df, table_name):
    engine = get_engine()
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows into '{table_name}'")