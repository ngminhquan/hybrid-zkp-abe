#Pydantic models
import sys
sys.path.insert(0, '/home/kupo/hybrid_zkp_abe')
from pydantic import BaseModel


class PhysPub(BaseModel):
    id: int
    att: str
    key_x: int
    key_y: int
    owner_id: str


    class Config:
        from_attributes = True


class PhysicalBase(BaseModel):
    att: str
    alpha: int

class PhysicalCreate(PhysicalBase):
    hash_phys: str
    key_x: int
    key_y: int
    owner_id: str

class Physical(PhysicalBase):
    id: int
    att: str
    alpha: int
    hash_phys: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    user_id: str

class UserCreate(BaseModel):
    pass

class User(UserBase):
    id: int
    user_id: str
    is_active: bool
    attributes: list[PhysPub] = []

class Verify_phys(BaseModel):
    user_id: str
    R_x: int
    iv: str
    ct: str