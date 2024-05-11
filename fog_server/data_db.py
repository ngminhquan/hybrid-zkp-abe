import sqlite3
db_path = '/home/kupo/hybrid_zkp_abe/fog_server/enc_data.db'
conn = sqlite3.connect(db_path)
columns = [
    "id INTEGER PRIMARY KEY",
    "user_id INTEGER UNIQUE",
    "enc_key VARCHAR",
    "cipher VARCHAR",
]
create_table_cmd = f"CREATE TABLE medicaldata ({','.join(columns)})"
conn.execute(create_table_cmd)
