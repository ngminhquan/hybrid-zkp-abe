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

#Generate administrator key pair
pzs = randint(1, 100)
Pzs = pzs * curve.g
def get_pzs():
    return pzs
def get_Pzs():
    return Pzs
