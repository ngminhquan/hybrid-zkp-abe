#Pydantic models
import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from pydantic import BaseModel


class DataBase(BaseModel):
    data_type: str
    enc_key: str
    cipher: str


class DataCreate(DataBase):
    proof: str


class Data(DataBase):
    id: int
    data_type: str
    enc_key: str
    cipher: str
    owner_id: int

    class Config:
        from_attributes = True


class CollectorBase(BaseModel):
    Collector_id: str


class CollectorCreate(CollectorBase):
    Di_x: str
    Di_y: str


class Collector(CollectorBase):
    id: int
    Di_x: str
    Di_y: str
    data: list[Data] = []

    class Config:
        from_attributes = True