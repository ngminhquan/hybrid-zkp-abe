import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fog_server import crud, models, schemas
from fog_server.data_db import SessionLocal, engine
import uvicorn
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/collectors/", response_model=schemas.Collector)
def create_collector(collector: schemas.CollectorCreate, db: Session = Depends(get_db)):
    db_collector = crud.get_collector_by_cid(db, cid=collector.Collector_id)
    if db_collector:
        raise HTTPException(status_code=400, detail="collector id already registered")
    return crud.create_collector(db=db, collector=collector)


@app.get("/collectors/", response_model=list[schemas.Collector])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    collectors = crud.get_collectors(db, skip=skip, limit=limit)
    return collectors


@app.get("/collectors/{user_id}", response_model=schemas.Collector)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_collector(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Collector not found")
    return db_user


@app.post("/collectors/{user_id}/data/", response_model=schemas.Data)
def create_data_for_collector(
    user_id: int, data: schemas.DataCreate, db: Session = Depends(get_db)
):
    return crud.create_collector_data(db=db, data=data, user_id=user_id)


@app.get("/data/", response_model=list[schemas.Data])
def read_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, skip=skip, limit=limit)
    return data

if __name__ == '__main__':
    uvicorn.run(app, port=8000)