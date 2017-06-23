import datetime
from flask import jsonify, request
from flask.views import MethodView, View
from session import session
from models import Keg, Beer, Kegerator

class KegView(MethodView):
    # Public
    def get(self, keg_id):
        if keg_id is None:
            result = []
            for instance in session.query(Keg).order_by(Keg.id):
                result.append(instance.to_json())
            return jsonify(result)
        else:
            keg = session.query(Keg).filter(Keg.id == keg_id).first()
            return jsonify(keg.to_json())

    # Admin
    def post(self):
        keg_json = request.get_json()

        try:
            keg = Keg(pints=keg_json['pints'], starting_pints=keg_json['starting_pints'], kegerator_ordinal=keg_json['kegerator_ordinal'])

            # TODO: Check for if the count will pass the kegerator max_count value and fail if so
            keg.kegerator = session.query(Kegerator).filter(Kegerator.id == int(keg_json['kegerator_id'])).first()
            keg.beer = session.query(Beer).filter(Beer.id == int(keg_json['beer_id'])).first()

            if keg.beer and keg.kegerator:
                session.add(keg)
                session.commit()
                return (jsonify(keg.to_json()), 201)
            else:
                return ('Beer or Kegerator not found', 400)
        except Exception as e:
            return ('Missing Parameters', 400)

    # Kegerator Who Owns it, or Admin
    def put(self, keg_id):
        keg_json = request.get_json()
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            if 'pints' in keg_json:
                keg.pints = keg_json['pints']

            if 'kegerator_ordinal' in keg_json:
                keg.kegerator_ordinal = keg_json['kegerator_ordinal']

            if 'unlocked_until' in keg_json:
                keg.unlocked_until = keg_json['unlocked_until']

            if 'locked_until' in keg_json:
                keg.locked_until = keg_json['locked_until']

            keg.updated_at = datetime.datetime.utcnow()

            session.commit()

            return jsonify(keg.to_json())
        else:
            return ('Keg Not Found', 404)

    # Admin
    def delete(self, keg_id):
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            session.delete(keg)
            session.commit()

            return ('', 204)
        else:
            return ('Keg Not Found', 404)

# Public
class ShowKegBeer(View):
    def dispatch_request(self, keg_id):
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            return jsonify(keg.beer.to_json())
        else:
            return ('Keg Not Found', 404)

# Public
class ShowKegKegerator(View):
    def dispatch_request(self, keg_id):
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            return jsonify(keg.kegerator.to_json())
        else:
            return ('Keg Not Found', 404)
