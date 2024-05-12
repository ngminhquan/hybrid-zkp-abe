#Pydantic models
from pydantic import BaseModel


class DataBase(BaseModel):
    data_type: str
    enc_key: str
    cipher: str


class DataCreate(DataBase):
    pass


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
    Di: str
    MAC: str


class Collector(CollectorBase):
    id: int
    Di: str
    MAC: str
    data: list[Data] = []

    class Config:
        from_attributes = True