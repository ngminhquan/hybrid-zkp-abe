import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from Crypto.Hash import SHA256
from ecc import field
from random import randint
from tinyec import registry

samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)
def int_to_bytes(num):
    # Xác định số byte cần thiết để lưu trữ số nguyên
    num_bytes = (num.bit_length() + 7) // 8
    # Chuyển đổi số nguyên thành chuỗi byte
    byte_string = num.to_bytes(num_bytes, byteorder='big')
    return byte_string
# Proof pi = (r*G, c, z) where r is random, c is the challenge, z is the proof
class Proof:
    def __init__(self, encrypted_random: field.Point, c: int, z: int):
        self.encrypted_random = encrypted_random
        self.c = c
        self.z = z

def proof2dict(proof: Proof):
    dict = {}
    dict['er_x'] = proof.encrypted_random.x
    dict['er_y'] = proof.encrypted_random.y
    dict['c'] = proof.c
    dict['z'] = proof.z
    return dict

def dict2proof(dict):
    proof = Proof(field.Point(curve, dict['er_x'], dict['er_y']), dict['c'], dict['z'])
    return proof
def zkp_generate(secret_info: int, ID: int):
    # random r and calc r*G
    r = randint(pow(2,254), pow(2,256))
    encrypted_r = r * curve.g

    # x*G
    public_info = secret_info * curve.g

    # challenge c = H(ID,g,g^r, g^x)
    c_bytes = SHA256.new(int_to_bytes(ID) + int_to_bytes(curve.g.x) + int_to_bytes(encrypted_r.x) + int_to_bytes(public_info.x)).digest()
    #c_bytes = SHA256.new(ID.encode() + int_to_bytes(curve.g.x) + int_to_bytes(encrypted_r.x) + int_to_bytes(public_info.x)).digest()
    c_int = int.from_bytes(c_bytes, byteorder='big')
    z = r + c_int * secret_info

    return Proof(encrypted_r, c_int, z)

def zkp_verify(proof: Proof, public_info: field.Point, ID: int):
    # Read value from received proof
    receive_encrypted_r = proof.encrypted_random
    receive_c = proof.c
    receive_z = proof.z
    # check if c is calculated correctly
    if receive_c == int.from_bytes(SHA256.new(int_to_bytes(ID) + int_to_bytes(curve.g.x) + int_to_bytes(receive_encrypted_r.x) + int_to_bytes(public_info.x)).digest(), byteorder='big'):
    #if receive_c == int.from_bytes(SHA256.new(ID.encode() + int_to_bytes(curve.g.x) + int_to_bytes(receive_encrypted_r.x) + int_to_bytes(public_info.x)).digest(), byteorder='big'):
        lhs = receive_z * curve.g
        rhs = receive_encrypted_r + receive_c * public_info
        # verify proof z (z*G =? r*G + c*x*G)
        if lhs == rhs:
            #print("Valid proof")
            return True
    #print("Invalid proof")
    return False

'''
real_info = 345
fake_info = 344
public_info = real_info * curve.g

zkproof_real = zkp_generate(real_info,'1')
zkproof_fake = zkp_generate(fake_info,'1')
print(zkp_verify(zkproof_real, public_info,'1'))
print(zkp_verify(zkproof_fake, public_info,'1'))
'''
