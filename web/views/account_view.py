import bcrypt
import datetime
from flask import jsonify, request, g
from flask.views import MethodView, View
from session import session
from models import Account, Card
from authenticate import requires_admin_auth

class AccountView(MethodView):

    @requires_admin_auth
    def index(self):
        result = []
        for instance in session.query(Account).order_by(Account.id):
            result.append(instance.to_json())
        return jsonify(result)

    @requires_admin_auth
    def show(self, account_id):
        account = session.query(Account).filter(Account.id == account_id).first()

        if account:
            return jsonify(account.to_json())
        else:
            return ('Account Not Found', 404)

    def get(self, account_id):
        if account_id is None:
            return self.index()
        else:
            return self.show(account_id)

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

    def link_card (self, account, email_token):
        card = session.query(Card).filter(Card.email_token == email_token).first()
        if card and account.email == card.email:
            card.account = account
            session.commit()
            return True
        else:
            return False

    @requires_admin_auth
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

            if 'email_token' in account_json:
                if not self.link_card(account, account_json['email_token']):
                    return ('Invalid Email Token', 400)

            return jsonify(account.to_json())
        else:
            return ('Account Not Found', 404)

    # Account, Admin
    @requires_admin_auth
    def delete(self, account_id):
        account = session.query(Account).filter(Account.id == account_id).first()

        if account:
            session.delete(account)
            session.commit()

            return ('', 204)
        else:
            return ('Account Not Found', 404)

class ShowAccountCards(View):
    @requires_admin_auth
    def dispatch_request(self, account_id):
        result = []
        account = session.query(Account).filter(Account.id == account_id).first()
        if account:
            for instance in account.cards:
                result.append(instance.to_json())
            return jsonify(result)
        else:
            return ('Account Not Found', 404)
