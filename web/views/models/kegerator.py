import uuid
import datetime
from base import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

class Kegerator(Base):
    __tablename__ = 'kegerator'
    id = Column(Integer, primary_key=True)
    max_kegs = Column(Integer)
    token = Column(String)
    secret = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def generate_secret (self):
        self.secret = uuid.uuid4()

    def generate_token (self):
        self.token = uuid.uuid4()

    def to_admin_json(self):
        return {
            'id': self.id,
            'max_kegs': self.max_kegs,
            'token': self.token,
            'secret': self.secret,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def to_json(self):
        return {
            'id': self.id,
            'max_kegs': self.max_kegs,
            'token': self.token,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def verify_secret(self, secret):
        return self.secret == secret

    def __repr__(self):
        return "<Kegerator(id='%s')>" % (self.id)
