import sys
sys.path.insert(0, './')
from random import randint
from tinyec import registry
from ecc import field
from Crypto.Hash import SHA256
from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import netifaces
import requests

def int_to_bytes(number):
    byte_length = (number.bit_length() + 7) // 8
    return number.to_bytes(byte_length, byteorder='big')
def encrypt_AES(key, plaintext):
    # Generate a random Initialization Vector (IV)
    iv = get_random_bytes(AES.block_size)
    
    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad the plaintext
    padded_plaintext = pad(plaintext, AES.block_size)
    
    # Encrypt the plaintext
    ciphertext = cipher.encrypt(padded_plaintext)
    
    # Return IV and ciphertext
    return iv, ciphertext
#Select an elliptic curve for the ECC-based protocol
samplecurve = registry.get_curve("brainpoolP256r1")
p = samplecurve.field.p
a = samplecurve.a
b = samplecurve.b
x_g = samplecurve.g.x
y_g = samplecurve.g.y
n = samplecurve.field.n
curve = field.Curve(a, b, p, n, x_g, y_g)

Pzs_url = 'http://127.0.0.1:9000/key/Pzs'
response = requests.get(Pzs_url)
if response.status_code == 200:
    Pzs = response.json()
    print(Pzs)
#random r and cal r*G
r = randint(2**254, 2**256)
R = r * curve.g 

k = SHA256.new(int_to_bytes(r*Pzs.x)).digest()