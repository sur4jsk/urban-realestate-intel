import sqlalchemy as sa
import pandas as pd

# Local connection
local_engine = sa.create_engine(
    "postgresql+psycopg2://postgres:realestate123@localhost:5432/realestate"
)

# Neon connection
neon_engine = sa.create_engine(
    "postgresql+psycopg2://neondb_owner:npg_AIcXn0ajsbS7@ep-young-union-ad8r9swu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

tables = ["macro_indicators", "news_sentiment"]

for table in tables:
    print(f"Migrating {table}...")
    df = pd.read_sql(f"SELECT * FROM {table}", local_engine)
    df.to_sql(table, neon_engine, if_exists="replace", index=False)
    print(f"Migrated {len(df)} rows to {table}")

print("Migration complete!")