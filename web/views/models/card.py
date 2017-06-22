import uuid
import datetime
import namesgenerator
from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String, default=namesgenerator.get_random_name())
    email = Column(String)
    rfid = Column(String, unique=True)
    credits = Column(Integer)
    email_token = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'rfid': self.rfid,
            'credits': self.credits,
            'email_token': self.email_token,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def generate_email_token(self):
        self.email_token = uuid.uuid4()

    def send_signup_email(self):
        print 'Email sent to %s with token %s' %(self.email, self.email_token)

    def __repr__(self):
        return "<Card(name='%s', email='%s', rfid='%s', credits='%s')>" %(self.name, self.email, self.rfid, str(self.credits))
