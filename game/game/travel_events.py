# game/travel_events.py

import random


def damage_player_percent(player, percent, minimum_damage=1):
    current_health = player.get("current_health", 100)

    damage = max(minimum_damage, round(current_health * percent))
    player["current_health"] = max(1, current_health - damage)

    return damage


def event_scorpion_sting(player, travel):
    damage = damage_player_percent(player, 0.80)

    return (
        "A scorpion crawls from beneath a warm stone and stings you!\n"
        f"You lose {damage} health.\n"
        f"Current health: {player['current_health']}."
    )


def event_heat_exhaustion(player, travel):
    damage = damage_player_percent(player, 0.20)

    return (
        "The sun beats down without mercy. Heat exhaustion slows your steps.\n"
        f"You lose {damage} health.\n"
        f"Current health: {player['current_health']}."
    )


def event_lost_in_dunes(player, travel):
    old_progress = travel.get("progress", 0)
    travel["progress"] = max(0, old_progress - 1)

    return (
        "The road disappears beneath wind-blown sand.\n"
        "You lose time finding your way back.\n"
        f"Travel progress is now {travel['progress']} / {travel['distance']}."
    )


def event_abandoned_pouch(player, travel):
    gold_found = random.randint(5, 25)
    player["gold"] = player.get("gold", 0) + gold_found

    return (
        "You notice a half-buried leather pouch near the roadside.\n"
        f"Inside, you find {gold_found} gold."
    )


def event_helpful_caravan(player, travel):
    reputation_gain = random.randint(1, 3)
    player["reputation"] = player.get("reputation", 0) + reputation_gain

    return (
        "You share the road with a friendly caravan for part of the journey.\n"
        f"Word of your good conduct spreads. Reputation +{reputation_gain}."
    )


TRAVEL_EVENTS = [
    {
        "id": "scorpion_sting",
        "name": "Scorpion Sting",
        "weight": 1,
        "min_danger": 2,
        "handler": event_scorpion_sting,
    },
    {
        "id": "heat_exhaustion",
        "name": "Heat Exhaustion",
        "weight": 3,
        "min_danger": 1,
        "handler": event_heat_exhaustion,
    },
    {
        "id": "lost_in_dunes",
        "name": "Lost in the Dunes",
        "weight": 3,
        "min_danger": 2,
        "handler": event_lost_in_dunes,
    },
    {
        "id": "abandoned_pouch",
        "name": "Abandoned Pouch",
        "weight": 2,
        "min_danger": 1,
        "handler": event_abandoned_pouch,
    },
    {
        "id": "helpful_caravan",
        "name": "Helpful Caravan",
        "weight": 2,
        "min_danger": 1,
        "handler": event_helpful_caravan,
    },
]


def get_possible_events(travel):
    danger = travel.get("danger", 1)

    return [
        event for event in TRAVEL_EVENTS
        if danger >= event.get("min_danger", 1)
    ]


def roll_travel_event(player, travel):
    danger = travel.get("danger", 1)

    # danger 1 = 8%
    # danger 2 = 11%
    # danger 3 = 14%
    # danger 4 = 17%
    event_chance = 5 + danger * 3

    roll = random.randint(1, 100)

    if roll > event_chance:
        return None

    possible_events = get_possible_events(travel)

    if not possible_events:
        return None

    weights = [event.get("weight", 1) for event in possible_events]
    chosen_event = random.choices(possible_events, weights=weights, k=1)[0]

    return chosen_event["handler"](player, travel)