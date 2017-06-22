import datetime
from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, ForeignKey('cards.email'), unique=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<Account(email='%s', name='%s, %s')>" %(self.name, self.last_name, self.first_name)
