#Alchemy models

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from zkp_server.phys_db import Base


class Physical(Base):
    __tablename__ = "attributes_private"

    id = Column(Integer, primary_key=True)
    att = Column(String, unique=True, index=True)
    alpha = Column(Integer)
    hash_phys = Column(String)


class Phys_public(Base):
    __tablename__ = "attributes_public"

    id = Column(Integer, primary_key=True)
    att = Column(String, ForeignKey("attributes_private.att"))
    key_x = Column(String, index=True)
    key_y = Column(String, index=True)