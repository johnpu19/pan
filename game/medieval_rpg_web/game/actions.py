from game.player import Player
from game.cities import CITIES
from game.enemies import generate_bandit, generate_mercenary, generate_rival_trader, generate_nomad_warrior, generate_assassin
import random
ENEMY_GENERATORS = {
    "Desert Bandit": generate_bandit,
    "Mercenary": generate_mercenary,
    "Rival Trader": generate_rival_trader,
    "Nomad Warrior": generate_nomad_warrior,
    "Assassin": generate_assassin,
}


def handle_action(action, player_data, item_name=None, quantity=1, destination=None):
    player = Player.load_from_dict(player_data)  # Convert dict to Player instance
    message = ""
    city_obj = CITIES[player.city]

    if action == "Buy":
        if item_name and city_obj.has_item(item_name):
            price = city_obj.get_buy_price(item_name) * quantity
            if player.gold >= price:
                player.gold -= price
                player.inventory[item_name] = player.inventory.get(item_name, 0) + quantity
                message = f"Bought {quantity} {item_name}(s) for {price} gold."
            else:
                message = "Not enough gold to buy."
        else:
            message = "Invalid item to buy."

    elif action == "Sell":
        if item_name and player.inventory.get(item_name, 0) >= quantity:
            price = city_obj.get_sell_price(item_name) * quantity
            player.inventory[item_name] -= quantity
            player.gold += price
            message = f"Sold {quantity} {item_name}(s) for {price} gold."
        else:
            message = "You don't have enough items to sell."

    elif action == "Travel":
        if destination and destination in CITIES:
            player.city = destination
            message = f"You traveled to {destination}."
        else:
            message = "Invalid destination."

    elif action == "Fight":
        if item_name in ENEMY_GENERATORS:
            enemy = ENEMY_GENERATORS[item_name]()
        else:
            enemy = random.choice(list(ENEMY_GENERATORS.values()))()

        fight_log = []

        while player.current_health > 0 and enemy.health > 0:
            player_damage = max(player.strength + random.randint(-2, 2), 0)
            enemy.health -= player_damage
            fight_log.append(f"You hit the {enemy.name} for {player_damage} damage! (Enemy HP: {max(enemy.health, 0)})")

            if enemy.health <= 0:
                fight_log.append(f"You defeated the {enemy.name}!")
                gold_reward = random.randint(15, 40)
                rep_reward = random.randint(1, 5)
                player.gold += gold_reward
                player.reputation += rep_reward
                fight_log.append(f"You earned {gold_reward} gold and {rep_reward} reputation.")
                break

            enemy_damage = max(enemy.attack + random.randint(-2, 2), 0)
            player.current_health -= enemy_damage
            fight_log.append(f"The {enemy.name} hits you for {enemy_damage} damage! (Your HP: {max(player.current_health, 0)})")

            if player.current_health <= 0:
                fight_log.append("You were defeated! Rest to recover your health.")
                break

        message = "\n".join(fight_log)

    elif action == "Rest":
        player.current_health = player.max_health
        message = "You have rested and restored your health."

    elif action == "Train":
        skill = item_name if item_name in ["strength", "intellect", "agility", "charisma", "endurance", "luck"] else None

        if skill == "strength":
            player.strength += 1
            message = "You feel stronger!"
        elif skill == "intellect":
            player.intellect += 1
            message = "You feel wiser!"
        elif skill == "agility":
            player.agility += 1
            message = "You feel more stretchy"
        elif skill == "charisma":
            player.charisma += 1
            message = "Others feel like you can, just because"
        elif skill == "endurance":
            player.endurance += 1
            message = "You feel not as out of breath"
        elif skill == "luck":
            player.luck += 1
            message = "You feel it will be a good day"
        else:
            message = "Unknown skill."

    else:
        message = "Unknown action."

    return message, player.to_dict()
