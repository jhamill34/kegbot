import bcrypt
import datetime
from flask import jsonify, request, g
from flask.views import MethodView
from session import session
from authenticate import requires_user_auth

class MyAccountView(MethodView):
    @requires_user_auth
    def get(self):
        return jsonify(g.account.to_json())

    def link_card (self, account, email_token):
        card = session.query(Card).filter(Card.email_token == email_token).first()
        if card and account.email == card.email:
            card.account = account
            session.commit()
            return True
        else:
            return False

    @requires_user_auth
    def put(self):
        account_json = request.get_json()
        account = g.account

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

    @requires_user_auth
    def delete(self):
        account = g.account

        session.delete(account)
        session.commit()

        return ('', 204)
