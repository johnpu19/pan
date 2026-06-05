import random

from .data import CITIES
from .map import MAP
from .travel import start_travel, continue_travel
from .items import create_item_instance
from .enemies import LOOT_TABLES
from .enemies import (
    generate_bandit,
    generate_mercenary,
    generate_rival_trader,
    generate_nomad_warrior,
    generate_assassin,
)
from .utils import compute_total_stats, get_trade_bonus
from .inventory_service import equip_item, unequip_item, sell_item, drop_item
from .caravan import buy_camel, sell_camel, load_cargo, unload_cargo

ENEMY_GENERATORS = {
    "Desert Bandit": generate_bandit,
    "Mercenary": generate_mercenary,
    "Rival Trader": generate_rival_trader,
    "Nomad Warrior": generate_nomad_warrior,
    "Assassin": generate_assassin,
}


DEFAULT_TRAVEL = {
    "active": False,
    "from": None,
    "to": None,
    "progress": 0,
    "distance": 0,
    "danger": 0,
    "route_name": None,
}


def normalize_city(player):
    """
    Internal city IDs should be lowercase:
    baghdad, damascus, aleppo, mosul
    """

    player["city"] = player.get("city", "baghdad").lower()

    if player["city"] not in MAP:
        player["city"] = "baghdad"

    return player["city"]


def get_market_for_player(player):
    """
    Bridge between lowercase MAP IDs and older CITIES keys like 'Baghdad'.
    """

    city_id = normalize_city(player)

    possible_keys = [
        city_id,
        city_id.title(),
        MAP.get(city_id, {}).get("name"),
    ]

    for key in possible_keys:
        if key in CITIES:
            return CITIES[key]

    return {}


def migrate_player(player):
    """
    Keeps old session saves compatible with current systems.
    """

    normalize_city(player)

    if "travel" not in player:
        player["travel"] = DEFAULT_TRAVEL.copy()

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

    if "gold" not in player:
        player["gold"] = 100

    if "reputation" not in player:
        player["reputation"] = 0

    return player


def handle_action(action, player, item_name=None, quantity=1, destination=None):
    player = migrate_player(player)
    market = get_market_for_player(player)

    message = ""

    # ----------------------------
    # BUY TRADE GOODS
    # ----------------------------
    if action == "Buy":
        if player["travel"]["active"]:
            message = "You cannot buy goods while traveling."

        elif not item_name or item_name not in market:
            message = "Invalid item to buy."

        else:
            base_price = market[item_name]["buy"]
            trade_bonus = get_trade_bonus(player)

            final_unit_price = max(1, round(base_price * (1 - trade_bonus)))
            total_price = final_unit_price * quantity

            if player["gold"] >= total_price:
                player["gold"] -= total_price
                player["trade_inventory"][item_name] = (
                    player["trade_inventory"].get(item_name, 0) + quantity
                )
                player["trade_xp"] += max(1, quantity)

                discount_percent = round(trade_bonus * 100, 1)
                message = (
                    f"Bought {quantity} {item_name}(s) for {total_price} gold "
                    f"({final_unit_price} each, {discount_percent}% trade bonus)."
                )
            else:
                message = f"Not enough gold to buy. You need {total_price} gold."

    # ----------------------------
    # SELL TRADE GOODS
    # ----------------------------
    elif action == "Sell":
        if player["travel"]["active"]:
            message = "You cannot sell goods while traveling."

        elif not item_name or item_name not in market:
            message = "Invalid item to sell here."

        elif player["trade_inventory"].get(item_name, 0) < quantity:
            message = "You don't have enough items to sell."

        else:
            base_price = market[item_name]["sell"]
            trade_bonus = get_trade_bonus(player)

            final_unit_price = max(1, round(base_price * (1 + trade_bonus)))
            total_price = final_unit_price * quantity

            player["trade_inventory"][item_name] -= quantity
            player["gold"] += total_price
            player["trade_xp"] += max(1, quantity * 2)

            bonus_percent = round(trade_bonus * 100, 1)
            message = (
                f"Sold {quantity} {item_name}(s) for {total_price} gold "
                f"({final_unit_price} each, +{bonus_percent}% trade bonus)."
            )

    # ----------------------------
    # MAP TRAVEL
    # ----------------------------
    elif action == "Travel":
        message = start_travel(player, destination)

    elif action == "Continue Travel":
        message = continue_travel(player)

    # ----------------------------
    # FIGHT
    # ----------------------------
    elif action == "Fight":
        if item_name in ENEMY_GENERATORS:
            enemy = ENEMY_GENERATORS[item_name]()
        else:
            enemy = random.choice(list(ENEMY_GENERATORS.values()))()

        stats = compute_total_stats(player)
        fight_log = []

        player_hit_chance = stats.get("hit_chance", 75)
        player_dodge_chance = stats.get("dodge_chance", 0)
        player_damage_min = stats.get("damage_min", 1)
        player_damage_max = stats.get("damage_max", 2)
        player_strength = stats.get("strength", 5)
        player_armor = stats.get("armor", 0)

        enemy_hit_chance = enemy.hit_chance
        enemy_dodge_chance = enemy.dodge_chance
        enemy_damage_min = enemy.damage_min
        enemy_damage_max = enemy.damage_max
        enemy_armor = enemy.armor

        while player["current_health"] > 0 and enemy.health > 0:
            # Player attack
            hit_roll = random.randint(1, 100)

            if hit_roll > player_hit_chance:
                fight_log.append(f"You miss the {enemy.name}!")
            else:
                dodge_roll = random.randint(1, 100)

                if dodge_roll <= enemy_dodge_chance:
                    fight_log.append(f"The {enemy.name} dodges your attack!")
                else:
                    raw_damage = (
                        random.randint(player_damage_min, player_damage_max)
                        + player_strength
                    )
                    final_damage = max(raw_damage - enemy_armor, 0)

                    enemy.health -= final_damage
                    fight_log.append(
                        f"You hit the {enemy.name} for {final_damage} damage! "
                        f"(Enemy HP: {max(enemy.health, 0)})"
                    )

            if enemy.health <= 0:
                fight_log.append(f"You defeated the {enemy.name}!")

                gold_reward = random.randint(enemy.gold_min, enemy.gold_max)
                rep_reward = random.randint(enemy.rep_min, enemy.rep_max)

                player["gold"] += gold_reward
                player["reputation"] += rep_reward

                fight_log.append(
                    f"You earned {gold_reward} gold and {rep_reward} reputation."
                )

                luck = stats.get("luck", 0)
                drop_chance = 25 + luck * 2
                roll = random.randint(1, 100)

                if roll <= drop_chance:
                    loot_list = LOOT_TABLES.get(enemy.name, [])

                    if loot_list:
                        template_id = random.choice(loot_list)
                        item = create_item_instance(template_id)

                        player["owned_items"][item["instance_id"]] = item
                        player["inventory_ids"].append(item["instance_id"])

                        from .items import get_template

                        template = get_template(template_id)
                        loot_name = template["name"] if template else template_id

                        fight_log.append(f"You found: {loot_name}!")
                    else:
                        fight_log.append("No item dropped.")
                else:
                    fight_log.append("No item dropped.")

                break

            # Enemy attack
            enemy_hit_roll = random.randint(1, 100)

            if enemy_hit_roll > enemy_hit_chance:
                fight_log.append(f"The {enemy.name} misses you!")
            else:
                player_dodge_roll = random.randint(1, 100)

                if player_dodge_roll <= player_dodge_chance:
                    fight_log.append(f"You dodge the {enemy.name}'s attack!")
                else:
                    enemy_raw_damage = random.randint(
                        enemy_damage_min, enemy_damage_max
                    )
                    enemy_final_damage = max(enemy_raw_damage - player_armor, 0)

                    player["current_health"] -= enemy_final_damage
                    fight_log.append(
                        f"The {enemy.name} hits you for {enemy_final_damage} damage! "
                        f"(Your HP: {max(player['current_health'], 0)})"
                    )

            if player["current_health"] <= 0:
                fight_log.append("You were defeated! Rest to recover your health.")
                break

        message = "\n".join(fight_log)

    # ----------------------------
    # REST
    # ----------------------------
    elif action == "Rest":
        stats = compute_total_stats(player)
        player["current_health"] = stats.get("max_health", 100)
        message = "You have rested and restored your health."

    elif action == "Visit Healer":
        if player["travel"]["active"]:
            message = "You cannot visit a healer while traveling."

        else:
            stats = compute_total_stats(player)
            max_health = stats.get("max_health", 100)
            current_health = player.get("current_health", max_health)

            missing_health = max_health - current_health

            if missing_health <= 0:
                message = "You are already at full health."

            else:
                healing_cost = max(10, missing_health)

                if player["gold"] >= healing_cost:
                    player["gold"] -= healing_cost
                    player["current_health"] = max_health

                    message = (
                        f"The healer treats your wounds.\n"
                        f"You paid {healing_cost} gold and restored your health to {max_health}."
                    )
                else:
                    message = (
                        f"You need {healing_cost} gold for treatment, "
                        f"but you only have {player['gold']}."
                    )

    # ----------------------------
    # TRAIN
    # ----------------------------
    elif action == "Train":
        valid_skills = ["strength", "agility", "vitality", "intellect"]
        skill = item_name if item_name in valid_skills else "strength"

        player["base_stats"][skill] += 1
        message = f"You improved your {skill} through training!"

    # ----------------------------
    # EQUIPMENT / INVENTORY
    # ----------------------------
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

    elif action == "SellItem":
        if item_name:
            success, result_message = sell_item(player, item_name)
            message = result_message
        else:
            message = "No item selected to sell."

    elif action == "DropItem":
        if item_name:
            success, result_message = drop_item(player, item_name)
            message = result_message
        else:
            message = "No item selected to drop."

    # ----------------------------
    # CARAVAN
    # ----------------------------
    elif action == "BuyCamel":
        message = buy_camel(player, quantity)

    elif action == "SellCamel":
        message = sell_camel(player, quantity)

    elif action == "LoadCargo":
        message = load_cargo(player, item_name, quantity)

    elif action == "UnloadCargo":
        message = unload_cargo(player, item_name, quantity)

    else:
        message = "Unknown action."

    return message, player
