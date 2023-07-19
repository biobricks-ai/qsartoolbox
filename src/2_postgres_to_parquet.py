import psycopg2, pandas as pd, os, sqlalchemy as sa
import pyarrow as pa, pyarrow.parquet as pq
from tqdm import tqdm

def get_table_names(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    return [table[0] for table in cur.fetchall()]

def get_row_count(conn, table_name):
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cur.fetchone()[0]

conn = psycopg2.connect(
    host="localhost",
    port=54321,
    dbname="mydatabase",
    user="myuser",
    password="mypassword"
)
table_names = get_table_names(conn)
table_info = []

engine = sa.create_engine('postgresql://myuser:mypassword@localhost:54321/mydatabase')

os.makedirs("brick", exist_ok=True)
def convert_table_to_parquet(conn, table_name):
    df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
    ocols = df.select_dtypes(include=['object']).columns
    df[ocols] = df[ocols].astype(str)    
    df.to_parquet(f"brick/{table_name}.parquet", engine='pyarrow')

# Convert each table to a Parquet file
pbar = tqdm(table_names)
for table in pbar:
    pbar.set_description(f"{table}")
    convert_table_to_parquet(conn, table)

