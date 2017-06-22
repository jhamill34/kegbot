from flask import jsonify, request
from flask.views import MethodView
from session import session
from models import User

class UserView(MethodView):
    def index(self):
        if 'rfid' in request.args:
            rfid = request.args.get('rfid')
            user = session.query(User).filter(User.rfid == rfid).first()
            if user:
                return jsonify(user.to_json())
            else:
                return ('User Not Found', 404)
        else:
            result = []
            for instance in session.query(User).order_by(User.id):
                result.append(instance.to_json())
            return jsonify(result)

    def show(self, user_id):
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            return jsonify(user.to_json())
        else:
            return ('User Not Found', 404)

    def get(self, user_id):
        if user_id is None:
            return self.index()
        else:
            return self.show(user_id)

    def post(self):
        usr_json = request.get_json()
        try:
            usr = User(name=usr_json['name'], tokens=usr_json['tokens'], rfid=usr_json['rfid'])
            session.add(usr)
            session.commit()
            return jsonify(usr.to_json())
        except Exception as e:
            return ('Missing parameters', 400)


    def delete(self, user_id):
        usr = session.query(User).filter(User.id == user_id).first()

        if usr:
            session.delete(usr)
            session.commit()

            return ('', 204)
        else:
            return ('User Not Found', 404)


    def put(self, user_id):
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
