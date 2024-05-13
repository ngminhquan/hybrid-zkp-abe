import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from charm.toolbox.pairinggroup import PairingGroup,GT, extract_key
from cpabe_xcrypt.cp_abe import abe
from ecc.zkp import zkp_generate, proof2dict, dict2proof, curve
import requests
import json
import netifaces
from Crypto.Hash import SHA256

def get_mac_address(interface="eth0"):
    mac_address = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    mac_address_bytes = bytes.fromhex(mac_address.replace(":", ""))
    return mac_address_bytes

#Connect: db cid -- policy
#input cid(user_id) function
user_id = 2
mac_address = get_mac_address()
print(mac_address)
cid = input('Enter collector ID:')
di = SHA256.new(cid.encode() + mac_address).digest()
proof_i = zkp_generate(int.from_bytes(di, byteorder='big'), user_id)
#print(proof_i.encrypted_random.x)
dict_proof = proof2dict(proof_i)
#print(dict2proof(dict_proof).encrypted_random.x)
#pi=int.from_bytes(di, byteorder='big') * curve.g

pumk_url = 'http://127.0.0.1:7000/key/pumk'
response = requests.get(pumk_url)
if response.status_code == 200:
    pumk = response.json()
    #print(pumk)

policy_A = '((a or b) and (c or d)) and (e or (f or (g and h))'
pairing_group = PairingGroup('SS512')
cpabe = abe(pairing_group)
msg = b'This is a message'
enc_key, cipher = cpabe.encrypt(pumk, msg, policy_A)
#print(enc_key, cipher)

# Dữ liệu cần gửi trong POST request
data = {
  "data_type": "string",
  "enc_key": json.dumps(enc_key),
  "cipher": json.dumps(cipher),
  "proof": json.dumps(dict_proof)
}

# Đường dẫn để thực hiện POST request
url = f"http://127.0.0.1:8000/collectors/{user_id}/data/"

# Thực hiện POST request và lấy response
response = requests.post(url, json=data)

# Hiển thị response
print("Response:", response.json())
