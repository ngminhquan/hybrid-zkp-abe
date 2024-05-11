#Define physical proof db
import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from random import randint
from tinyec import registry
from ecc import field
import sqlite3
import random
from Crypto.Hash import SHA256
#Select an elliptic curve for the ECC-based protocol
samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)
import sqlite3
conn = sqlite3.connect("phys_proof.db")
columns = [
    "id INTEGER PRIMARY KEY",
    "Attribute VARCHAR UNIQUE",
    "key_x NUMBER",
    "key_y NUMBER",
    "Details VARCHAR",
]
create_table_cmd = f"CREATE TABLE prooff ({','.join(columns)})"
conn.execute(create_table_cmd)

#Add data

import sqlite3
import random
from Crypto.Hash import SHA256
conn = sqlite3.connect("phys_proof.db")
omega = ['Doctor1', 'Doctor2', 'Nurse1', 'Nurse2']
phys = []
for i in range(len(omega)):
    alpha = random.randint(1, 100)
    key = alpha * curve.g
    phys.append(f"{i}, '{omega[i]}', {key.x}, {key.y}, '{SHA256.new(omega[i].encode()).digest().hex()}'")
for person_data in phys:
    insert_cmd = f"INSERT INTO prooff VALUES ({person_data})"
    conn.execute(insert_cmd)
conn.commit()
