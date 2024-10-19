import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine

# Koneksi ke BigQuery
service_account = "/home/kudadiri/.dbt/dbt-project-data.json"
client = bigquery.Client.from_service_account_json(service_account)

project, dataset, table = "resources-node", "titanic_dataset", "dataset"
table_ref = client.dataset(dataset, project=project).table(table)
table = client.get_table(table_ref)
df = client.list_rows(table).to_dataframe()

# Koneksi ke PostgreSQL
user = 'postgres'
password = 'diy3times'
host = 'localhost'
database = 'postgres'
port = 5432
link = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(link)

# Mengisi nilai kosong dan menghapus baris dengan nilai NaN
age_average = round(df['age'].mean())
df.fillna({
    'age': age_average,
    'cabin': 'Unknown',
    'boat': 'No Boat',
    'body': 0,
    'home_dest': 'Unknown'
}, inplace=True)
df.dropna(inplace=True)

# Membuat skrip SQL
table_name = 'titanic_cleaned'
create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    age INTEGER,
    cabin VARCHAR,
    boat VARCHAR,
    body INTEGER,
    home_dest VARCHAR
);
"""

insert_data_sql = f"INSERT INTO {table_name} (age, cabin, boat, body, home_dest) VALUES\n"

# Menambahkan data dari DataFrame ke pernyataan INSERT
values_list = []
for index, row in df.iterrows():
    values_list.append(f"({row['age']}, '{row['cabin']}', '{row['boat']}', {row['body']}, '{row['home_dest']}')")
insert_data_sql += ",\n".join(values_list) + ";"

# Menyimpan skrip SQL ke file
with open('models/create_titanic_cleaned.sql', 'w') as file:
    file.write(create_table_sql)
    file.write("\n")
    file.write(insert_data_sql)

print("File SQL berhasil dibuat: create_titanic_cleaned.sql")
