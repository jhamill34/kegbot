from flask import jsonify, request
from flask.views import MethodView
from session import session
from models import Kegerator

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

    def post(self):
        kegerator_json = request.get_json()
        try:
            kegerator = Kegerator()
            session.add(kegerator)
            session.commit()

            return jsonify(kegerator.to_json())
        except Exception as e:
            return ('Missing Parameters', 400)

    def put(self, kegerator_id):
        kegerator_json = request.get_json()
        kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()
        if kegerator:
            # session.commit()
            return jsonify(kegerator.to_json())
        else:
            return ('Kegerator Not Found', 404)

    def delete(self, kegerator_id):
        kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()

        if kegerator:
            session.delete(kegerator)
            session.commit()

            return ('', 204)
        else:
            return ('Kegerator Not Found', 404)

# @app.route('/kegerator/<int:kegerator_id>/kegs')
# def show_kegerator_kegs(kegerator_id):
#     kegerator = session.query(Kegerator).filter(Kegerator.id == kegerator_id).first()
#
#     if kegerator:
#         result = []
#         for instance in kegerator.kegs:
#             result.append(instance.to_json())
#         return jsonify(result)
#     else:
#         return ('Kegerator Not Found', 404)
