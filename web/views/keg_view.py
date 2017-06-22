from flask import jsonify, request
from flask.views import MethodView, View
from session import session
from models import Keg, Beer, Kegerator

class KegView(MethodView):
    def get(self, keg_id):
        if keg_id is None:
            result = []
            for instance in session.query(Keg).order_by(Keg.id):
                result.append(instance.to_json())
            return jsonify(result)
        else:
            keg = session.query(Keg).filter(Keg.id == keg_id).first()
            return jsonify(keg.to_json())

    def post(self):
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

    def put(self, keg_id):
        keg_json = request.get_json()
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            if 'pints' in keg_json:
                keg.pints = keg_json['pints']

            session.commit()

            return jsonify(keg.to_json())
        else:
            return ('Keg Not Found', 404)

    def delete(self, keg_id):
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            session.delete(keg)
            session.commit()

            return ('', 204)
        else:
            return ('Keg Not Found', 404)


class ShowKegBeer(View):
    def dispatch_request(self, keg_id):
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            return jsonify(keg.beer.to_json())
        else:
            return ('Keg Not Found', 404)

class ShowKegKegerator(View):
    def dispatch_request(self, keg_id):
        keg = session.query(Keg).filter(Keg.id == keg_id).first()

        if keg:
            return jsonify(keg.kegerator.to_json())
        else:
            return ('Keg Not Found', 404)
