#Test physical proof data

import sqlite3
pridb_path = '/home/kupo/hybrid_zkp_abe/zkp_server/private_phys.db'
proofdb_path = '/home/kupo/hybrid_zkp_abe/zkp_server/proof.db'
conn = sqlite3.connect(proofdb_path)
cur = conn.cursor()
cur.execute("SELECT * FROM proof")


people = cur.fetchall()
for person in people:
    print(person)
