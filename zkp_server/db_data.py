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
#Define an attribute set, publish ω and verification keys
pridb_path = '/home/kupo/hybrid_zkp_abe/zkp_server/private_phys.db'
proofdb_path = '/home/kupo/hybrid_zkp_abe/zkp_server/proof.db'
pri_conn = sqlite3.connect(pridb_path)

omega = ['Doctor1', 'Doctor2', 'Nurse1', 'Nurse2']
pri = []
phys = []

for i in range(len(omega)):
    alpha = randint(1, 100)
    key = alpha * curve.g
    pri.append(f"{i}, '{omega[i]}', {alpha}, '{SHA256.new(omega[i].encode()).digest().hex()}'")
    phys.append(f"{i}, '{omega[i]}', {key.x}, {key.y}")

for person_data in pri:
    insert_cmd = f"INSERT INTO priproof VALUES ({person_data})"
    pri_conn.execute(insert_cmd)
pri_conn.commit()

conn = sqlite3.connect(proofdb_path)
for person_data in phys:
    insert_cmd = f"INSERT INTO proof VALUES ({person_data})"
    conn.execute(insert_cmd)
conn.commit()
