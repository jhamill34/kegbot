import datetime
from flask import jsonify, request
from flask.views import MethodView
from session import session
from models import Card

class CardView(MethodView):
    # Admin
    def index(self):
        if 'rfid' in request.args:
            rfid = request.args.get('rfid')
            card = session.query(Card).filter(Card.rfid == rfid).first()
            if card:
                return jsonify(card.to_json())
            else:
                return ('Card Not Found', 404)
        else:
            result = []
            for instance in session.query(Card).order_by(Card.id):
                result.append(instance.to_json())
            return jsonify(result)

    # Admin
    def show(self, card_id):
        card = session.query(Card).filter(Card.id == card_id).first()
        if card:
            return jsonify(card.to_json())
        else:
            return ('Card Not Found', 404)

    # --- Inherit ---
    def get(self, card_id):
        if card_id is None:
            return self.index()
        else:
            return self.show(card_id)

    # Admin
    def post(self):
        card_json = request.get_json()
        try:
            card = Card(email=card_json['email'], credits=card_json['credits'], rfid=card_json['rfid'])
            card.generate_email_token()
            session.add(card)
            session.commit()
            card.send_signup_email()
            return (jsonify(card.to_json()), 201)
        except Exception as e:
            return ('Missing parameters: %s' % (str(e)), 400)

    # Admin
    def delete(self, card_id):
        card = session.query(Card).filter(Card.id == card_id).first()

        if card:
            session.delete(card)
            session.commit()

            return ('', 204)
        else:
            return ('Card Not Found', 404)

    # Admin
    def put(self, card_id):
        card_json = request.get_json()
        card = session.query(Card).filter(Card.id == card_id).first()

        if card:
            if 'email' in card_json:
                card.name = card_json['email']

            if 'rfid' in card_json:
                card.rfid = card_json['rfid']

            if 'credits' in card_json:
                card.tokens = card_json['credits']

            card.updated_at = datetime.datetime.utcnow()

            session.commit()

            return jsonify(card.to_json())
        else:
            return ('Card Not Found', 404)
