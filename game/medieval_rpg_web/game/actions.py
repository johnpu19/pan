from game.data import CITIES
from game.enemies import generate_bandit, generate_mercenary, generate_rival_trader, generate_nomad_warrior, generate_assassin
import random

ENEMY_GENERATORS = {
    "Desert Bandit": generate_bandit,
    "Mercenary": generate_mercenary,
    "Rival Trader": generate_rival_trader,
    "Nomad Warrior": generate_nomad_warrior,
    "Assassin": generate_assassin,
}

def handle_action(action, player, item_name=None, quantity=1, destination=None):
    message = ""

    if action == "Buy":
        if item_name and item_name in CITIES[player['city']]:
            price = CITIES[player['city']][item_name]['buy'] * quantity
            if player['gold'] >= price:
                player['gold'] -= price
                player['inventory'][item_name] = player['inventory'].get(item_name, 0) + quantity
                message = f"Bought {quantity} {item_name}(s) for {price} gold."
            else:
                message = "Not enough gold to buy."
        else:
            message = "Invalid item to buy."

    elif action == "Sell":
        if item_name and player['inventory'].get(item_name, 0) >= quantity:
            price = CITIES[player['city']][item_name]['sell'] * quantity
            player['inventory'][item_name] -= quantity
            player['gold'] += price
            message = f"Sold {quantity} {item_name}(s) for {price} gold."
        else:
            message = "You don't have enough items to sell."

    elif action == "Travel":
        if destination and destination in CITIES:
            player['city'] = destination
            message = f"You traveled to {destination}."
        else:
            message = "Invalid destination."

    elif action == "Fight":
        if item_name in ENEMY_GENERATORS:
            enemy = ENEMY_GENERATORS[item_name]()
        else:
            enemy = random.choice(list(ENEMY_GENERATORS.values()))()

        fight_log = []

        while player['health'] > 0 and enemy.health > 0:
            player_damage = max(player['strength'] + random.randint(-2, 2), 0)
            enemy.health -= player_damage
            fight_log.append(f"You hit the {enemy.name} for {player_damage} damage! (Enemy HP: {max(enemy.health, 0)})")

            if enemy.health <= 0:
                fight_log.append(f"You defeated the {enemy.name}!")
                gold_reward = random.randint(15, 40)
                rep_reward = random.randint(1, 5)
                player['gold'] += gold_reward
                player['reputation'] += rep_reward
                fight_log.append(f"You earned {gold_reward} gold and {rep_reward} reputation.")
                break

            enemy_damage = max(enemy.attack + random.randint(-2, 2), 0)
            player['health'] -= enemy_damage
            fight_log.append(f"The {enemy.name} hits you for {enemy_damage} damage! (Your HP: {max(player['health'], 0)})")

            if player['health'] <= 0:
                fight_log.append("You were defeated! Rest to recover your health.")
                break

        message = "<br>".join(fight_log)
    
    elif action == "Rest":
        player['health'] = 100  # or max health
        message = "You have rested and restored your health."

    else:
        message = "Unknown action."

    return message, player
