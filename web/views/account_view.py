import bcrypt
import datetime
from flask import jsonify, request
from flask.views import MethodView
from session import session
from models import Account, Card

class AccountView(MethodView):
    # Account, Admin
    def get(self, account_id):
        if account_id is None:
            result = []
            for instance in session.query(Account).order_by(Account.id):
                result.append(instance.to_json())
            return jsonify(result)
        else:
            account = session.query(Account).filter(Account.id == account_id).first()

            if account:
                return jsonify(account.to_json())
            else:
                return ('Account Not Found', 404)

    # Public
    def post(self):
        account_json = request.get_json()
        try:
            hashed_pwd = bcrypt.hashpw(str(account_json['password']), bcrypt.gensalt())
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
            return ('Missing parameters: %s' %(e), 400)

    # Account, Admin
    def put(self, account_id):
        account_json = request.get_json()
        account = session.query(Account).filter(Account.id == account_id).first()

        if account:
            account.updated_at = datetime.datetime.utcnow()

            if 'email' in account_json:
                account.email = account_json['email']

            if 'first_name' in account_json:
                account.first_name = account_json['first_name']

            if 'last_name' in account_json:
                account.last_name = account_json['last_name']

            session.commit()

            return jsonify(account.to_json())
        else:
            return ('Account Not Found', 404)

    # Account, Admin
    def delete(self, account_id):
        account = session.query(Account).filter(Account.id == account_id).first()

        if account:
            session.delete(account)
            session.commit()

            return ('', 204)
        else:
            return ('Account Not Found', 404)
