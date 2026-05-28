from flask import Flask, render_template, request, session, redirect, url_for

from game.player import Player
from game.items import ITEM_TEMPLATES, create_item_instance
from game.actions import handle_action
from game.data import CITIES
from game.utils import compute_total_stats, get_trade_bonus
from game.map import MAP
from game.travel import get_available_destinations


app = Flask(__name__)
app.secret_key = "sultan-secret-key"


DEFAULT_TRAVEL = {
    "active": False,
    "from": None,
    "to": None,
    "progress": 0,
    "distance": 0,
    "danger": 0,
    "route_name": None,
}


def normalize_player(player):
    """
    Keeps old saves compatible with the newer map/travel system.
    Internal city IDs are lowercase: baghdad, damascus, aleppo, mosul.
    """

    player["city"] = player.get("city", "baghdad").lower()

    if player["city"] not in MAP:
        player["city"] = "baghdad"

    if "travel" not in player:
        player["travel"] = DEFAULT_TRAVEL.copy()

    if "base_stats" not in player:
        player["base_stats"] = {
            "strength": player.get("strength", 5),
            "agility": 5,
            "vitality": 5,
            "intellect": player.get("intellect", 5),
            "luck": 3,
        }

    if "current_health" not in player:
        player["current_health"] = 50 + player["base_stats"].get("vitality", 5) * 10

    if "trade_xp" not in player:
        player["trade_xp"] = 0

    if "trade_inventory" not in player:
        player["trade_inventory"] = {
            "Spices": 0,
            "Silk": 0,
            "Dates": 0,
            "Carpets": 0,
            "Incense": 0,
        }

    if "owned_items" not in player:
        player["owned_items"] = {}

    if "inventory_ids" not in player:
        player["inventory_ids"] = []

    if "equipment" not in player:
        player["equipment"] = {
            "weapon": None,
            "head": None,
            "chest": None,
            "ring_1": None,
            "ring_2": None,
        }

    return player


def get_player():
    if "player" not in session:
        new_player = Player("Traveler")
        session["player"] = new_player.to_dict()

    player = normalize_player(session["player"])
    session["player"] = player
    return player


def get_market(city_id):
    """
    Bridge between lowercase map IDs and older CITIES keys like 'Baghdad'.
    """

    possible_keys = [
        city_id,
        city_id.title(),
        MAP.get(city_id, {}).get("name"),
    ]

    for key in possible_keys:
        if key in CITIES:
            return CITIES[key]

    return {}


@app.route("/")
def index():
    player = get_player()

    city = player["city"]
    market = get_market(city)

    message = session.pop("message", None)
    total_stats = compute_total_stats(player)
    trade_bonus = get_trade_bonus(player)

    available_destinations = {}
    if not player["travel"]["active"]:
        available_destinations = get_available_destinations(player)

    return render_template(
        "index.html",
        player=player,
        city=city,
        market=market,
        CITIES=CITIES,
        MAP=MAP,
        message=message,
        ITEM_TEMPLATES=ITEM_TEMPLATES,
        total_stats=total_stats,
        trade_bonus=trade_bonus,
        available_destinations=available_destinations,
    )


@app.route("/action", methods=["POST"])
def action():
    player_data = get_player()

    action_name = request.form.get("action")
    item_name = request.form.get("item") or request.form.get("item_name")
    destination = request.form.get("destination")

    try:
        quantity = int(request.form.get("quantity", 1))
        if quantity < 1:
            quantity = 1
    except (TypeError, ValueError):
        quantity = 1

    result = handle_action(
        action_name,
        player_data,
        item_name=item_name,
        quantity=quantity,
        destination=destination,
    )

    # Supports both styles:
    # return message
    # return message, player
    if isinstance(result, tuple):
        message, updated_player = result
    else:
        message = result
        updated_player = player_data

    updated_player = normalize_player(updated_player)

    session["player"] = updated_player
    session["message"] = message

    return redirect(url_for("index"))


@app.route("/reset")
def reset():
    session.clear()
    return "Session cleared. Go back to <a href='/'>home</a>."


@app.route("/give_item")
def give_item():
    player = get_player()

    item = create_item_instance("iron_scimitar")

    player["owned_items"][item["instance_id"]] = item
    player["inventory_ids"].append(item["instance_id"])

    session["player"] = normalize_player(player)

    return "Gave Iron Scimitar. Go back to <a href='/'>home</a>."


if __name__ == "__main__":
    app.run(debug=True)