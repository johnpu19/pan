# game/travel.py

from .map import MAP
from .travel_events import roll_travel_event


DEFAULT_TRAVEL = {
    "active": False,
    "from": None,
    "to": None,
    "progress": 0,
    "distance": 0,
    "danger": 0,
    "route_name": None,
}


def reset_travel():
    return DEFAULT_TRAVEL.copy()


def get_available_destinations(player):
    city_id = player.get("city", "baghdad").lower()

    if city_id not in MAP:
        city_id = "baghdad"
        player["city"] = city_id

    return MAP[city_id]["connections"]


def start_travel(player, destination_id):
    current_city = player.get("city", "baghdad").lower()

    if current_city not in MAP:
        current_city = "baghdad"
        player["city"] = current_city

    if "travel" not in player:
        player["travel"] = reset_travel()

    if player["travel"]["active"]:
        return "You are already traveling."

    if not destination_id:
        return "No destination selected."

    if destination_id not in MAP[current_city]["connections"]:
        return "You cannot travel there from here."

    route = MAP[current_city]["connections"][destination_id]

    player["travel"] = {
        "active": True,
        "from": current_city,
        "to": destination_id,
        "progress": 0,
        "distance": route["distance"],
        "danger": route["danger"],
        "route_name": route["route_name"],
    }

    return f"You leave {MAP[current_city]['name']} for {MAP[destination_id]['name']}."


def continue_travel(player):
    if "travel" not in player:
        player["travel"] = reset_travel()

    travel = player["travel"]

    if not travel["active"]:
        return "You are not currently traveling."

    messages = []

    travel["progress"] += 1

    messages.append(f"You continue along the {travel['route_name']}.")

    event_message = roll_travel_event(player, travel)

    if event_message:
        messages.append(event_message)

    if travel["progress"] >= travel["distance"]:
        destination = travel["to"]

        player["city"] = destination
        player["travel"] = reset_travel()

        messages.append(f"You arrive in {MAP[destination]['name']}.")

    return "\n".join(messages)