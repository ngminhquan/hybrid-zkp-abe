#Alchemy models

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from fog_server.data_db import Base


class Collector(Base):
    __tablename__ = "collectors"

    id = Column(Integer, primary_key=True)
    Collector_id = Column(String, unique=True, index=True)
    Di_x = Column(String)
    Di_y = Column(String)

    data = relationship("Data", back_populates="owner")


class Data(Base):
    __tablename__ = "medical_data"

    id = Column(Integer, primary_key=True)
    data_type = Column(String, index=True)
    enc_key = Column(String, index=True)
    cipher = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("collectors.id"))

    owner = relationship("Collector", back_populates="data")