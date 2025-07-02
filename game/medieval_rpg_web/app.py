from flask import Flask, render_template, request, session
from game.player import Player
from game.actions import handle_action
from game.cities import CITIES 


app = Flask(__name__)
app.secret_key = 'sultan-secret-key'

def get_player():
    if 'player' not in session or not isinstance(session['player'].get('inventory'), dict) or 'city' not in session['player']:
        session['player'] = Player("Traveler").__dict__
    return session['player']

@app.route('/')
def index():
    player = get_player()
    city = player['city']
    market = CITIES[city]
    message = session.pop('message', None)  # Show message once then remove it
    return render_template("index.html", player=player, market=market, city=city, CITIES=CITIES, message=message)

@app.route('/action', methods=['POST'])
def action():
    action = request.form['action']
    player_data = session['player']

    # Check for item_name or item because form uses both in different places
    item_name = request.form.get('item') or request.form.get('item_name')
    quantity = request.form.get('quantity', 1)
    destination = request.form.get('destination')

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1

    message, updated_player = handle_action(action, player_data, item_name=item_name, quantity=quantity, destination=destination)
    session['player'] = updated_player

    city = updated_player['city']
    market = CITIES[city]

    return render_template("index.html", player=updated_player, city=city, market=market, CITIES=CITIES, message=message)

@app.route('/reset')
def reset():
    session.clear()
    return "Session cleared. Go back to <a href='/'>home</a>."

if __name__ == "__main__":
    app.run(debug=True)
