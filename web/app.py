from flask import Flask
from views import *
from utils import WebUtils

app = Flask(__name__)

util = WebUtils(app)

util.register_api(CardView, 'card_api', '/cards', pk='card_id')
util.register_api(KegeratorView, 'kegerator_api', '/kegerators', pk='kegerator_id')
util.register_api(BeerView, 'beer_api', '/beers', pk='beer_id')
util.register_api(KegView, 'keg_api', '/kegs', pk='keg_id')
util.register_api(KegView, 'account_api', '/accounts', pk='account_id')

app.add_url_rule('/beers/<int:beer_id>/kegs', view_func=ShowBeerKegs.as_view('show_beer_kegs'))
app.add_url_rule('/kegerators/<int:kegerator_id>/kegs', view_func=ShowKegeratorKegs.as_view('show_kegerator_kegs'))
app.add_url_rule('/kegs/<int:keg_id>/beer', view_func=ShowKegBeer.as_view('show_keg_beer'))
app.add_url_rule('/kegs/<int:keg_id>/kegerator', view_func=ShowKegKegerator.as_view('show_keg_kegerator'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
