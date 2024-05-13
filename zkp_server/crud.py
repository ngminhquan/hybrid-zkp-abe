import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from sqlalchemy.orm import Session
from zkp_server import models, schemas
from ecc.zkp import zkp_verify, curve, dict2proof
from ecc.field import Point
import json
from random import randint

def get_physical(db: Session, id: int):
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