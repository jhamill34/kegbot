import bcrypt
import datetime
from flask import jsonify, request
from flask.views import MethodView
from session import session
from models import Account, User

class AccountView(MethodView):
    # Account, Admin
    def get(self, account_id):
        pass

    # Public
    def post(self):
        account_json = request.get_json()
        try:
            hashed_pwd = bcrypt.hashpw(account_json['password'], bcrypt.gensalt())
            account = Account(
                email=account_json['email'],
                first_name=account_json['first_name'],
                last_name=account_json['last_name'],
                password=hashed_pwd
            )
            session.add(account)
            session.commit()
            return (jsonify(account.to_json()), 201)
        except Exception as e:
            return ('Missing parameters', 400)

    # Account, Admin
    def delete(self, account_id):
        pass

    # Account, Admin
    def put(self, account_id):
        pass
