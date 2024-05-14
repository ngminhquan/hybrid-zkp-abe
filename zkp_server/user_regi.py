import sys
sys.path.insert(0, './')
from random import randint
from tinyec import registry
from ecc import field
from Crypto.Hash import SHA256
from random import randint
from Crypto.Cipher import AES
from cpabe_xcrypt.AES_CBC import int_to_bytes, encrypt_AES, decrypt_AES
import netifaces
import requests
import json


user_id = '1234'
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
dict_ai = {'A1':'phyA1', 'A2':'phyA2'}
#encrypt
data = json.dumps(dict_ai)
iv,ciphertext = encrypt_AES(k,data.encode())

# Dữ liệu cần gửi trong POST request
data = {'user_id': user_id,
        'R_x': R.x,
        'iv': iv, 
        'ct': ciphertext}

#Đường dẫn để thực hiện POST request
url = f"http://127.0.0.1:9000/registration/"

# Thực hiện POST request và lấy response
response = requests.post(url, json=data)

# Hiển thị response
print("Response:", response.json())


