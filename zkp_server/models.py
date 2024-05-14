#Alchemy models

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from zkp_server.phys_db import Base


class Physical(Base):
    __tablename__ = "attributes_private"

    id = Column(Integer, primary_key=True)
    att = Column(String, index=True)
    alpha = Column(Integer)
    hash_phys = Column(String)



class Phys_public(Base):
    __tablename__ = "attributes_public"

    id = Column(Integer, primary_key=True)
    att = Column(String, ForeignKey("attributes_private.att"))
    key_x = Column(Integer, index=True)
    key_y = Column(Integer, index=True)

    owner_id = Column(Integer, ForeignKey("users.user_id"))
    owner = relationship("User", back_populates="attributes")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    is_active = Column(Boolean, default=True)

    attributes = relationship("Phys_public", back_populates="owner")
