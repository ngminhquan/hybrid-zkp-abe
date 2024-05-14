import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from sqlalchemy.orm import Session
from zkp_server import models, schemas
from ecc.zkp import zkp_verify, curve, dict2proof, zkp_generate
from cpabe_xcrypt.AES_CBC import int_to_bytes, encrypt_AES, decrypt_AES
from ecc.field import Point
from Crypto.Hash import SHA256
import json
from random import randint

def get_physical_by_id(db: Session, id: int):
    return db.query(models.Physical).filter(models.Physical.id == id).first()


def get_physical_by_att(db: Session, att: str):
    return db.query(models.Physical).filter(models.Physical.att == att).first()


def get_all_physical(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Physical).offset(skip).limit(limit).all()


def create_physical(db: Session, physical: schemas.PhysicalCreate):
    hash_phys = physical.hash_phys
    key_x = physical.key_x
    key_y = physical.key_y
    db_physical = models.Physical(att=physical.att, alpha=physical.alpha, hash_phys=hash_phys)
    db_pub = models.Phys_public(att=physical.att, key_x=key_x, key_y=key_y)
    db.add(db_physical)
    db.add(db_pub)
    db.commit()
    db.refresh(db_physical)
    db.refresh(db_pub)
    return db_physical


def get_physpub(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Phys_public).offset(skip).limit(limit).all()

#Generate administrator key pair
pzs = randint(1, 100)
Pzs = pzs * curve.g
def get_pzs():
    return pzs
def get_Pzs(Pzs):
    return Pzs

def verify_phys(db: Session, user_data: schemas.Verify_phys):
    user_id = user_data.user_id
    R_x = user_data.R_x
    iv = user_data.iv
    ct = user_data.ct
    k_new = SHA256.new(R_x*pzs)
    plaintext = decrypt_AES(k_new,iv,ct)
    dict_ai = json.loads(plaintext)
    proof_dict = {}
    #key: att; value: physical proof
    for key, value in dict_ai.items():
        phys = db.query(models.Physical).filter(models.Physical.att == key).first()
        alpha = phys.alpha
        hash_phys = phys.hash_phys
        hash_val = SHA256.new(value.encode()).digest() 
        #if hash_val == hash_phys:
        if hash_phys == '1':
        #proof_dict = {'A1' :{'enc_r':encrypted_r.x,'c': c_int,'z':z,'A': A1 }}
            proof_dict[key] = zkp_generate(alpha,user_id,key)
        else:
            return None
    proof_dict_json = json.dumps(proof_dict)
    ct = encrypt_AES(k_new,proof_dict_json.encode())#bytes
    return ct