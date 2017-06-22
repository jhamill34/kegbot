import datetime
from base import Base
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rfid = Column(String, unique=True)
    tokens = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'rfid': self.rfid,
            'tokens': self.tokens,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<User(name='%s', rfid='%s', tokens='%s')>" %(self.name, self.rfid, str(self.tokens))
