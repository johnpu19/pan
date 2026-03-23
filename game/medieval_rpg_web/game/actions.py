from .data import CITIES
import random
from .enemies import (
    generate_bandit,
    generate_mercenary,
    generate_rival_trader,
    generate_nomad_warrior,
    generate_assassin,
)
from .utils import compute_total_stats
from .inventory_service import equip_item, unequip_item

ENEMY_GENERATORS = {
    "Desert Bandit": generate_bandit,
    "Mercenary": generate_mercenary,
    "Rival Trader": generate_rival_trader,
    "Nomad Warrior": generate_nomad_warrior,
    "Assassin": generate_assassin,
}


def handle_action(action, player, item_name=None, quantity=1, destination=None):
    message = ""

    # safety migration for older session data
    if "trade_inventory" not in player:
        player["trade_inventory"] = {
            "Spices": 0,
            "Silk": 0,
            "Dates": 0,
            "Carpets": 0,
            "Incense": 0,
        }

    if "base_stats" not in player:
        player["base_stats"] = {
            "strength": 5,
            "agility": 5,
            "vitality": 5,
            "intellect": 5,
            "luck": 3,
        }

    if "current_health" not in player:
        player["current_health"] = 50 + player["base_stats"].get("vitality", 5) * 10

    if "trade_xp" not in player:
        player["trade_xp"] = 0

    if action == "Buy":
        if item_name and item_name in CITIES[player["city"]]:
            price = CITIES[player["city"]][item_name]["buy"] * quantity
            if player["gold"] >= price:
                player["gold"] -= price
                player["trade_inventory"][item_name] = player["trade_inventory"].get(item_name, 0) + quantity
                player["trade_xp"] += max(1, price // 10)
                message = f"Bought {quantity} {item_name}(s) for {price} gold."
            else:
                message = "Not enough gold to buy."
        else:
            message = "Invalid item to buy."

    elif action == "Sell":
        if item_name and player["trade_inventory"].get(item_name, 0) >= quantity:
            price = CITIES[player["city"]][item_name]["sell"] * quantity
            player["trade_inventory"][item_name] -= quantity
            player["gold"] += price
            player["trade_xp"] += max(1, price // 10)
            message = f"Sold {quantity} {item_name}(s) for {price} gold."
        else:
            message = "You don't have enough items to sell."

    elif action == "Travel":
        if destination and destination in CITIES:
            player["city"] = destination
            message = f"You traveled to {destination}."
        else:
            message = "Invalid destination."

    elif action == "Fight":
        if item_name in ENEMY_GENERATORS:
            enemy = ENEMY_GENERATORS[item_name]()
        else:
            enemy = random.choice(list(ENEMY_GENERATORS.values()))()

        # transitional combat: use total stats, but keep system simple
        stats = compute_total_stats(player)
        fight_log = []

        while player["current_health"] > 0 and enemy.health > 0:
            player_damage = max(stats.get("strength", 5) + random.randint(-2, 2), 0)
            enemy.health -= player_damage
            fight_log.append(
                f"You hit the {enemy.name} for {player_damage} damage! "
                f"(Enemy HP: {max(enemy.health, 0)})"
            )

            if enemy.health <= 0:
                fight_log.append(f"You defeated the {enemy.name}!")
                gold_reward = random.randint(15, 40)
                rep_reward = random.randint(1, 5)
                player["gold"] += gold_reward
                player["reputation"] += rep_reward
                fight_log.append(f"You earned {gold_reward} gold and {rep_reward} reputation.")
                break

            enemy_damage = max(enemy.attack + random.randint(-2, 2), 0)
            player["current_health"] -= enemy_damage
            fight_log.append(
                f"The {enemy.name} hits you for {enemy_damage} damage! "
                f"(Your HP: {max(player['current_health'], 0)})"
            )

            if player["current_health"] <= 0:
                fight_log.append("You were defeated! Rest to recover your health.")
                break

        message = "\n".join(fight_log)

    elif action == "Rest":
        stats = compute_total_stats(player)
        player["current_health"] = stats.get("max_health", 100)
        message = "You have rested and restored your health."

    elif action == "Train":
        valid_skills = ["strength", "agility", "vitality", "intellect"]
        skill = item_name if item_name in valid_skills else "strength"
        player["base_stats"][skill] += 1
        message = f"You improved your {skill} through training!"
    
    elif action == "Equip":
        if item_name:
            success, result_message = equip_item(player, item_name)
            message = result_message
        else:
            message = "No item selected to equip."

    elif action == "Unequip":
        if item_name:
            success, result_message = unequip_item(player, item_name)
            message = result_message
        else:
            message = "No slot selected to unequip."

    else:
        message = "Unknown action."

    return message, player