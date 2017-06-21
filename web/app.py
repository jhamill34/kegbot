import os
import datetime
import json
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Unicode, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine_string = 'postgresql://docker:mysecretpassword@db:5432/kegbot'
engine = create_engine(engine_string)

Base = declarative_base()

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
class Kegerator(Base):
    __tablename__ = 'kegerator'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow())

    def to_json(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<Kegerator(id='%s')>" % (self.id)

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

Beer.kegs = relationship('Keg', order_by=Keg.id, back_populates='beer')
Kegerator.kegs = relationship('Keg', order_by=Keg.id, back_populates='kegerator')

Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


app = Flask(__name__)

''' USER ROUTES '''
@app.route('/users')
def users():
    result = []
    for instance in session.query(User).order_by(User.id):
        result.append(instance.to_json())
    return jsonify(result)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        return jsonify(user.to_json())
    else:
        return ('User Not Found', 404)

@app.route('/users', methods=['POST'])
def create_user():
    usr_json = request.get_json()
    try:
        usr = User(name=usr_json['name'], tokens=usr_json['tokens'], rfid=usr_json['rfid'])
        session.add(usr)
        session.commit()
        return jsonify(usr.to_json())
    except Exception as e:
        return ('Missing parameters', 400)


@app.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id):
    usr_json = request.get_json()
    usr = session.query(User).filter(User.id == user_id).first()

    if usr:
        if 'name' in usr_json:
            usr.name = usr_json['name']

        if 'rfid' in usr_json:
            usr.rfid = usr_json['rfid']

        if 'tokens' in usr_json:
            usr.tokens = usr_json['tokens']

        session.commit()

        return jsonify(usr.to_json())
    else:
        return ('User Not Found', 404)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    usr = session.query(User).filter(User.id == user_id).first()

    if usr:
        session.delete(usr)
        session.commit()

        return ('', 204)
    else:
        return ('User Not Found', 404)

''' BEER ROUTES '''
@app.route('/beer')
def beers():
    result = []
    for instance in session.query(Beer).order_by(Beer.id):
        result.append(instance.to_json())
    return jsonify(result)

@app.route('/beer/<int:beer_id>')
def show_beer(beer_id):
    beer = session.query(Beer).filter(Beer.id == beer_id).first()

    if beer:
        return jsonify(beer.to_json())
    else:
        return ('Beer Not Found', 404)

@app.route('/beer', methods=['POST'])
def create_beer():
    beer_json = request.get_json()

    try:
        beer = Beer(name=beer_json['name'], description=beer_json['description'])
        session.add(beer)
        session.commit()

        return jsonify(beer.to_json())
    except Exception as e:
        return ('Missing Parameters', 400)

@app.route('/beer/<int:beer_id>', methods=['PUT', 'PATCH'])
def update_beer(beer_id):
    beer_json = request.get_json()
    beer = session.query(Beer).filter(Beer.id == beer_id).first()

    if beer:
        if 'name' in beer_json:
            beer.name = beer_json['name']

        if 'description' in beer_json:
            beer.description = beer_json['description']

        session.commit()

        return jsonify(beer.to_json())
    else:
        return ('Beer Not Found', 404)

@app.route('/beer/<int:beer_id>', methods=['DELETE'])
def delete_beer(beer_id):
    beer = session.query(Beer).filter(Beer.id == beer_id).first()

    if beer:
        session.delete(beer)
        session.commit()

        return ('', 204)
    else:
        return ('Beer Not Found', 404)


@app.route('/beer/<int:beer_id>/kegs')
def show_beer_kegs(beer_id):
    beer = session.query(Beer).filter(Beer.id == beer_id).first()
    if beer:
        result = []
        for instance in beer.kegs:
            result.append(instance.to_json())
        return jsonify(result)
    else:
        return ('Beer Not Found', 404)

''' KEGERATOR ROUTES '''
@app.route('/kegerator')
def kegerators():
    result = []
    for instance in session.query(Kegerator).order_by(Kegerator.id):
        result.append(instance.to_json())
    return jsonify(result)

@app.route('/kegerator/<int:kegerator_id>')
def show_kegerator(kegerator_id):
    kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()
    if kegerator:
        return jsonify(kegerator.to_json())
    else:
        return ('Kegerator Not Found', 404)

@app.route('/kegerator', methods=['POST'])
def create_kegerator():
    kegerator_json = request.get_json()
    try:
        kegerator = Kegerator()
        session.add(kegerator)
        session.commit()

        return jsonify(kegerator.to_json())
    except Exception as e:
        return ('Missing Parameters', 400)

@app.route('/kegerator/<int:kegerator_id>', methods=['PUT', 'PATCH'])
def update_kegerator(kegerator_id):
    kegerator_json = request.get_json()
    kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()
    if kegerator:
        # session.commit()
        return jsonify(kegerator.to_json())
    else:
        return ('Kegerator Not Found', 404)

@app.route('/kegerator/<int:kegerator_id>', methods=['DELETE'])
def delete_kegerator(kegerator_id):
    kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()

    if kegerator:
        session.delete(kegerator)
        session.commit()

        return ('', 204)
    else:
        return ('Kegerator Not Found', 404)


@app.route('/kegerator/<int:kegerator_id>/kegs')
def show_kegerator_kegs(kegerator_id):
    kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()

    if kegerator:
        result = []
        for instance in kegerator.kegs:
            result.append(instance.to_json())
        return jsonify(result)
    else:
        return ('Kegerator Not Found', 404)

''' KEG ROUTES '''
@app.route('/keg')
def kegs():
    result = []
    for instance in session.query(Keg).order_by(Keg.id):
        result.append(instance.to_json())
    return jsonify(result)

@app.route('/keg/<int:keg_id>')
def show_keg(keg_id):
    keg = session.query(Keg).filter(Keg.id == keg_id).first()
    return jsonify(keg.to_json())

@app.route('/keg', methods=['POST'])
def create_keg():
    keg_json = request.get_json()

    try:
        keg = Keg(pints=keg_json['pints'], starting_pints=keg_json['starting_pints'])

        keg.kegerator = session.query(Kegerator).filter(Kegerator.id == int(keg_json['kegerator_id'])).first()
        keg.beer = session.query(Beer).filter(Beer.id == int(keg_json['beer_id'])).first()

        if keg.beer and keg.kegerator:
            session.add(keg)
            session.commit()
            return jsonify(keg.to_json())
        else:
            return ('Beer or Kegerator not found', 400)
    except Exception as e:
        return ('Missing Parameters', 400)

@app.route('/keg/<int:keg_id>', methods=['PUT', 'PATCH'])
def update_keg(keg_id):
    keg_json = request.get_json()
    keg = session.query(Keg).filter(Keg.id == keg_id).first()

    if keg:
        if 'pints' in keg_json:
            keg.pints = keg_json['pints']

        session.commit()

        return jsonify(keg.to_json())
    else:
        return ('Keg Not Found', 404)

@app.route('/keg/<int:keg_id>', methods=['DELETE'])
def delete_keg(keg_id):
    keg = session.query(Keg).filter(Keg.id == keg_id).first()

    if keg:
        session.delete(keg)
        session.commit()

        return ('', 204)
    else:
        return ('Keg Not Found', 404)

@app.route('/keg/<int:keg_id>/beer')
def show_keg_beer(keg_id):
    keg = session.query(Keg).filter(Keg.id == keg_id).first()

    if keg:
        return jsonify(keg.beer.to_json())
    else:
        return ('Keg Not Found', 404)

@app.route('/keg/<int:keg_id>/kegerator')
def show_keg_kegerator(keg_id):
    keg = session.query(Keg).filter(Keg.id == keg_id).first()

    if keg:
        return jsonify(keg.kegerator.to_json())
    else:
        return ('Keg Not Found', 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
