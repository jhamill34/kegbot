from flask import jsonify, request
from flask.views import MethodView, View
from session import session
from models import Kegerator
from authenticate import requires_admin_auth

class KegeratorView(MethodView):
    def get(self, kegerator_id):
        if kegerator_id is None:
            result = []
            for instance in session.query(Kegerator).order_by(Kegerator.id):
                result.append(instance.to_json())
            return jsonify(result)
        else:
            kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()
            if kegerator:
                return jsonify(kegerator.to_json())
            else:
                return ('Kegerator Not Found', 404)

    @requires_admin_auth
    def post(self):
        kegerator_json = request.get_json()
        try:
            kegerator = Kegerator(max_kegs=kegerator_json['max_kegs'])
            kegerator.generate_secret()
            kegerator.generate_token()

            session.add(kegerator)
            session.commit()

            return (jsonify(kegerator.to_admin_json()), 201)
        except Exception as e:
            return ('Missing Parameters: %s' %(e), 400)

    @requires_admin_auth
    def put(self, kegerator_id):
        kegerator_json = request.get_json()
        kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()
        if kegerator:
            if 'max_kegs' in kegerator_json:
                kegerator.max_kegs = kegerator_json['max_kegs']

            session.commit()
            return jsonify(kegerator.to_json())
        else:
            return ('Kegerator Not Found', 404)

    @requires_admin_auth
    def delete(self, kegerator_id):
        kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()

        if kegerator:
            session.delete(kegerator)
            session.commit()

            return ('', 204)
        else:
            return ('Kegerator Not Found', 404)

class ShowKegeratorKegs(View):
    def dispatch_request(self, kegerator_id):
        kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()

        if kegerator:
            result = []
            # TODO: Order by the ordinal values
            for instance in kegerator.kegs:
                result.append(instance.to_json())
            return jsonify(result)
        else:
            return ('Kegerator Not Found', 404)
