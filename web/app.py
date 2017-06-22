from flask import Flask
from views import BeerView, KegView, KegeratorView, UserView

app = Flask(__name__)

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk), view_func=view_func, methods=['GET', 'PUT', 'DELETE'])

register_api(UserView, 'user_api', '/users', pk='user_id')
register_api(KegeratorView, 'kegerator_api', '/kegerators', pk='kegerator_id')
register_api(BeerView, 'beer_api', '/beers', pk='beer_id')
register_api(KegView, 'keg_api', '/kegs', pk='keg_id')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
