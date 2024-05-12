from sqlalchemy.orm import Session

from fog_server import models, schemas


def get_collector(db: Session, id: int):
    return db.query(models.Collector).filter(models.Collector.id == id).first()


def get_collector_by_cid(db: Session, cid: str):
    return db.query(models.Collector).filter(models.Collector.Collector_id == cid).first()


def get_collectors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Collector).offset(skip).limit(limit).all()


def create_collector(db: Session, collector: schemas.CollectorCreate):
    Di = collector.Di
    db_collector = models.Collector(Collector_id=collector.Collector_id, Di=Di, MAC=collector.MAC)
    db.add(db_collector)
    db.commit()
    db.refresh(db_collector)
    return db_collector


def get_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Data).offset(skip).limit(limit).all()


def create_collector_data(db: Session, data: schemas.DataCreate, user_id: int):
    db_data = models.Data(**data.model_dump(), owner_id=user_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data