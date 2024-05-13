#Pydantic models
import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from pydantic import BaseModel


class PhysPubBase(BaseModel):
    att: str


class PhysPub(PhysPubBase):
    id: int
    att: str
    key_x: int
    key_y: int

    class Config:
        from_attributes = True


class PhysicalBase(BaseModel):
    att: str
    alpha: int


class PhysicalCreate(PhysicalBase):
    hash_phys: str
    key_x: int
    key_y: int


class Physical(PhysicalBase):
    id: int
    att: str
    alpha: int
    hash_phys: str


    class Config:
        from_attributes = True