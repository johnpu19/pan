from flask import Flask, render_template, request, session
from game.player import Player
from game.items import ITEM_TEMPLATES
from game.actions import handle_action
from game.data import CITIES
from game.utils import compute_total_stats
from game.items import create_item_instance

app = Flask(__name__)
app.secret_key = 'sultan-secret-key'


def get_player():
    if 'player' not in session:
        player = Player("Traveler")
        session['player'] = player.to_dict()
        return session['player']

    player = session['player']

    if 'city' not in player:
        player['city'] = "Baghdad"

    if 'base_stats' not in player:
        player['base_stats'] = {
            "strength": player.get("strength", 5),
            "agility": 5,
            "vitality": 5,
            "intellect": player.get("intellect", 5),
            "luck": 3,
        }

    if 'current_health' not in player:
        player['current_health'] = 50 + player['base_stats'].get("vitality", 5) * 10

    if 'trade_xp' not in player:
        player['trade_xp'] = 0

    if 'trade_inventory' not in player:
        player['trade_inventory'] = {
            "Spices": 0,
            "Silk": 0,
            "Dates": 0,
            "Carpets": 0,
            "Incense": 0,
        }

    if 'owned_items' not in player:
        player['owned_items'] = {}

    if 'inventory_ids' not in player:
        player['inventory_ids'] = []

    if 'equipment' not in player:
        player['equipment'] = {
            "weapon": None,
            "head": None,
            "chest": None,
            "ring_1": None,
            "ring_2": None,
        }

    session['player'] = player
    return player


@app.route('/')
def index():
    player = get_player()
    city = player['city']
    market = CITIES[city]
    message = session.pop('message', None)
    total_stats = compute_total_stats(player)

    return render_template(
        "index.html",
        player=player,
        market=market,
        city=city,
        CITIES=CITIES,
        message=message,
        ITEM_TEMPLATES=ITEM_TEMPLATES,
        total_stats=total_stats
    )


@app.route('/action', methods=['POST'])
def action():
    action = request.form['action']
    player_data = session['player']

    item_name = request.form.get('item') or request.form.get('item_name')
    quantity = request.form.get('quantity', 1)
    destination = request.form.get('destination')

    try:
        quantity = int(quantity)
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1

    message, updated_player = handle_action(
        action,
        player_data,
        item_name=item_name,
        quantity=quantity,
        destination=destination
    )
    session['player'] = updated_player

    city = updated_player['city']
    market = CITIES[city]
    total_stats = compute_total_stats(updated_player)

    return render_template(
        "index.html",
        player=updated_player,
        city=city,
        market=market,
        CITIES=CITIES,
        message=message,
        ITEM_TEMPLATES=ITEM_TEMPLATES,
        total_stats=total_stats
    )


@app.route('/reset')
def reset():
    session.clear()
    return "Session cleared. Go back to <a href='/'>home</a>."

@app.route('/give_item')
def give_item():
    player = get_player()

    item = create_item_instance("iron_scimitar")

    player["owned_items"][item["instance_id"]] = item
    player["inventory_ids"].append(item["instance_id"])

    session["player"] = player

    return "Gave Iron Scimitar. Go back to <a href='/'>home</a>."


if __name__ == "__main__":
    app.run(debug=True)