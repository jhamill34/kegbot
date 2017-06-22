import datetime
from flask import jsonify, request
from flask.views import MethodView, View
from session import session
from models import Beer

class BeerView(MethodView):
    def get(self, beer_id):
        if beer_id is None:
            result = []
            for instance in session.query(Beer).order_by(Beer.id):
                result.append(instance.to_json())
            return jsonify(result)
        else:
            beer = session.query(Beer).filter(Beer.id == beer_id).first()

            if beer:
                return jsonify(beer.to_json())
            else:
                return ('Beer Not Found', 404)

    def post(self):
        beer_json = request.get_json()

        try:
            beer = Beer(name=beer_json['name'], description=beer_json['description'])
            session.add(beer)
            session.commit()

            return jsonify(beer.to_json())
        except Exception as e:
            return ('Missing Parameters', 400)

    def put(self, beer_id):
        beer_json = request.get_json()
        beer = session.query(Beer).filter(Beer.id == beer_id).first()

        if beer:
            if 'name' in beer_json:
                beer.name = beer_json['name']

            if 'description' in beer_json:
                beer.description = beer_json['description']

            beer.updated_at = datetime.datetime.utcnow()

            session.commit()

            return jsonify(beer.to_json())
        else:
            return ('Beer Not Found', 404)

    def delete(self, beer_id):
        beer = session.query(Beer).filter(Beer.id == beer_id).first()

        if beer:
            session.delete(beer)
            session.commit()

            return ('', 204)
        else:
            return ('Beer Not Found', 404)

class ShowBeerKegs(View):
    def dispatch_request(self, beer_id):
        beer = session.query(Beer).filter(Beer.id == beer_id).first()
        if beer:
            result = []
            for instance in beer.kegs:
                result.append(instance.to_json())
            return jsonify(result)
        else:
            return ('Beer Not Found', 404)
