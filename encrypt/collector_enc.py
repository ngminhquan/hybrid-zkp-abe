import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from charm.toolbox.pairinggroup import PairingGroup,GT, extract_key
from cpabe_xcrypt.cp_abe import abe
from ecc.zkp import zkp_generate
import requests
import json

idi = 1
di = 2
proof_i = zkp_generate(di, idi)

pumk_url = 'http://127.0.0.1:8000/key/pumk'
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