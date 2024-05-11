import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from charm.toolbox.pairinggroup import PairingGroup, G1, G2, GT, extract_key
from cpabe_xcrypt.cp_abe import abe
import json
group = PairingGroup('SS512')
cpabe = abe(group)
#Setup algorithm to generate public key PK and master key MK
(pumk, pmk) = cpabe.setup()

def get_pmk():
    return pmk
def get_pumk():
    return pumk

