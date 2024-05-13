import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from sqlalchemy.orm import Session
from fog_server import models, schemas
from ecc.zkp import zkp_verify, curve, dict2proof
from ecc.field import Point
import json

def get_collector(db: Session, id: int):
    return db.query(models.Collector).filter(models.Collector.id == id).first()


def get_collector_by_cid(db: Session, cid: str):
    return db.query(models.Collector).filter(models.Collector.Collector_id == cid).first()


def get_collectors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Collector).offset(skip).limit(limit).all()


def create_collector(db: Session, collector: schemas.CollectorCreate):
    Di_x = collector.Di_x
    Di_y = collector.Di_y
    db_collector = models.Collector(Collector_id=collector.Collector_id, Di_x=Di_x, Di_y=Di_y)
    db.add(db_collector)
    db.commit()
    db.refresh(db_collector)
    return db_collector


def get_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Data).offset(skip).limit(limit).all()


def create_collector_data(db: Session, data: schemas.DataCreate, user_id: int):
    dict_proof = json.loads(data.proof)
    user_proof = dict2proof(dict_proof)
    clt = db.query(models.Collector).filter(models.Collector.id == user_id).first()
    public_info = Point(curve, int(clt.Di_x), int(clt.Di_y))
    verify = zkp_verify(user_proof, public_info, user_id)
    if verify:
        db_data = models.Data(**data.model_dump(exclude={"proof"}), owner_id=user_id)
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data
    else:
        return None