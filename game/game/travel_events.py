# game/travel_events.py

import random


def event_scorpion_sting(player, travel):
    """
    Scorpion sting travel event.
    Removes 80% of current health, but does not kill the player outright.
    """

    current_health = player.get("current_health", 100)

    damage = max(1, round(current_health * 0.8))
    player["current_health"] = max(1, current_health - damage)

    return (
        "A scorpion crawls from beneath a warm stone and stings you!\n"
        f"You lose {damage} health.\n"
        f"Current health: {player['current_health']}."
    )


TRAVEL_EVENTS = [
    {
        "id": "scorpion_sting",
        "name": "Scorpion Sting",
        "weight": 1,
        "min_danger": 1,
        "handler": event_scorpion_sting,
    },
]


def get_possible_events(travel):
    danger = travel.get("danger", 1)

    return [
        event for event in TRAVEL_EVENTS
        if danger >= event.get("min_danger", 1)
    ]


def roll_travel_event(player, travel):
    """
    Rolls whether an event happens during travel.
    Higher route danger = higher event chance.
    """

    danger = travel.get("danger", 1)

    # Example:
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