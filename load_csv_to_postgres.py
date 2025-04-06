import pandas as pd
from sqlalchemy import create_engine

# --- Config ---
CSV_PATH = "data.csv"  csv
DB_USER = "root"
DB_PASSWORD = "root"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "fire_detection_dataset"
TABLE_NAME = "fire_sensor_satellite_data"

# --- Load CSV ---
print("Reading dataset...")
df = pd.read_csv(CSV_PATH)

# Optional: preview
print("Preview:")
print(df.head())

# --- Connect to PostgreSQL ---
print("Connecting to database...")
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# --- Insert data ---
print(f"Inserting data into table '{TABLE_NAME}'...")
df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)

print("Data successfully loaded into PostgreSQL!")
