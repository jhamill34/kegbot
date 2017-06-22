import datetime
from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Unicode

class Beer(Base):
    __tablename__ = 'beer'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(Unicode(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<Beer(name='%s')>" % (self.name)
