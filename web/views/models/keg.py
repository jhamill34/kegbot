import datetime
import beer, kegerator
from base import Base
from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship

class Keg(Base):
    __tablename__ = 'keg'
    id = Column(Integer, primary_key=True)
    pints = Column(Numeric)
    starting_pints = Column(Numeric)
    beer_id = Column(Integer, ForeignKey('beer.id'))
    kegerator_id = Column(Integer, ForeignKey('kegerator.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    beer = relationship('Beer', back_populates='kegs')
    kegerator = relationship('Kegerator', back_populates='kegs')

    def to_json(self):
        return {
            'id': self.id,
            'pints': str(self.pints),
            'starting_pints': str(self.starting_pints),
            'beer_id': self.beer_id,
            'kegerator_id': self.kegerator_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<Keg(pints='%s', starting_pints='%s', beer='%s', kegerator='%s')>" % (self.pints, self.starting_pints, str(self.beer_id), str(self.kegerator_id))

beer.Beer.kegs = relationship('Keg', order_by=Keg.id, back_populates='beer')
kegerator.Kegerator.kegs = relationship('Keg', order_by=Keg.id, back_populates='kegerator')
