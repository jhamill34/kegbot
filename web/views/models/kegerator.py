import datetime
from base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

class Kegerator(Base):
    __tablename__ = 'kegerator'
    id = Column(Integer, primary_key=True)
    max_kegs = Column(Integer)
    secret = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def to_json(self):
        return {
            'id': self.id,
            'max_kegs': self.max_kegs,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<Kegerator(id='%s')>" % (self.id)
