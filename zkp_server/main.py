import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from zkp_server import crud, models, schemas
from zkp_server.phys_db import SessionLocal, engine
from ecc.zkp import curve
from random import randint
import json
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

#Create a new attribute with hash(physical proof)
@app.post("/physical/", response_model=schemas.Physical)
def create_physical(physical: schemas.PhysicalCreate, db: Session = Depends(get_db)):
    db_physical = crud.get_physical_by_att(db, att=physical.att)
    if db_physical:
        raise HTTPException(status_code=400, detail="physical already registered")
    pub = crud.create_physical(db=db, physical=physical)
    return pub


#Read all attributes and physical proof
@app.get("/physical/", response_model=list[schemas.Physical])
def read_all_physical(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    physical = crud.get_all_physical(db, skip=skip, limit=limit)
    return physical


#Read all attributes and 
@app.get("/physpub/", response_model=list[schemas.PhysPub])
def read_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_physpub(db, skip=skip, limit=limit)
    return data


#Read attribute by id
@app.get("/physical/{phys_id}", response_model=schemas.Physical)
def read_user(phys_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_physical_by_id(db, id=phys_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Attribute not found")
    else:
        return db_user
 



#Generate administrator key pair
pzs = randint(1, 100)
Pzs = pzs * curve.g
@app.get("/key/Pzs", response_model=None)
def get_Pzs():
    dict = {}
    dict['Pzs.x'] = Pzs.x
    dict['Pzs.y'] = Pzs.y
    return json.dumps(dict)

#user registration -> ZKP
@app.connect("/registration", response_model=None)
def verify_phys(user_data: schemas.Verify_phys):
    data = verify_phys(user_data)    
    return data

if __name__ == '__main__':
    uvicorn.run(app, port=9000)