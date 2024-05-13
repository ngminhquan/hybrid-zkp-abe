#Define physical proof db
import sqlite3
pridb_path = '/home/kupo/hybrid_zkp_abe/zkp_server/private_phys.db'
proofdb_path = '/home/kupo/hybrid_zkp_abe/zkp_server/proof.db'
pri_conn = sqlite3.connect(pridb_path)
columns = [
    "id INTEGER PRIMARY KEY",
    "Attribute VARCHAR UNIQUE",
    "alpha NUMBER",
    "Details VARCHAR",
]
create_table_cmd = f"CREATE TABLE priproof ({','.join(columns)})"
pri_conn.execute(create_table_cmd)


conn = sqlite3.connect(proofdb_path)
columns = [
    "id INTEGER PRIMARY KEY",
    "Attribute VARCHAR UNIQUE",
    "key_x NUMBER",
    "key_y NUMBER",
]
create_table_cmd = f"CREATE TABLE proof ({','.join(columns)})"
conn.execute(create_table_cmd)