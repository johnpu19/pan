# game/actions.py
from game.data import CITIES
from game.enemies import Enemy, generate_bandit
import random

def process_action(action, player, item_name=None, quantity=1):
    city = player['city']
    market = CITIES[city]
    message = ""

    if action == 'Buy':
        price = market.get(item_name, {}).get('buy')
        if price and player['gold'] >= price * quantity:
            player['gold'] -= price * quantity
            player['inventory'][item_name] = player['inventory'].get(item_name, 0) + quantity
            message = f"Bought {quantity} {item_name}(s) for {price * quantity} gold."
        else:
            message = f"Cannot buy {item_name}."

    elif action == 'Sell':
        price = market.get(item_name, {}).get('sell')
        if price and player['inventory'].get(item_name, 0) >= quantity:
            player['gold'] += price * quantity
            player['inventory'][item_name] -= quantity
            message = f"Sold {quantity} {item_name}(s) for {price * quantity} gold."
        else:
            message = f"Cannot sell {item_name}."

    elif action == 'Travel':
        destination = item_name
        if destination in CITIES:
            player['city'] = destination
            message = f"You traveled to {destination}."
        else:
            message = "Unknown destination."

    elif action == 'Train':
        player['strength'] += 1
        message = "You trained and gained 1 strength."

    elif action == 'Rest':
        player['health'] = 100
        message = "You rested and fully restored your health."

    


    if action == 'Fight':
        # Generate an enemy — you can extend this logic to generate other enemy types
        if item_name == "Desert Bandit" or item_name is None:
            enemy = generate_bandit()
        else:
            # fallback enemy or extend with other generators
            enemy = generate_bandit()

        fight_log = []

        while player['health'] > 0 and enemy.health > 0:
            # Player attacks enemy
            player_damage = max(player['strength'] + random.randint(-2, 2), 0)
            enemy.health -= player_damage
            fight_log.append(f"You hit the {enemy.name} for {player_damage} damage! (Enemy HP: {max(enemy.health, 0)})")

            if enemy.health <= 0:
                fight_log.append(f"You defeated the {enemy.name}!")
                gold_reward = random.randint(15, 30)
                rep_reward = random.randint(1, 3)
                player['gold'] += gold_reward
                player['reputation'] += rep_reward
                fight_log.append(f"You earned {gold_reward} gold and {rep_reward} reputation.")
                break

            # Enemy attacks player
            enemy_damage = max(enemy.attack + random.randint(-2, 2), 0)
            player['health'] -= enemy_damage
            fight_log.append(f"The {enemy.name} hits you for {enemy_damage} damage! (Your HP: {max(player['health'], 0)})")

            if player['health'] <= 0:
                fight_log.append("You were defeated! Rest to recover your health.")
                break

        message = "".join(fight_log)

   
    return message, player



    return message, player

