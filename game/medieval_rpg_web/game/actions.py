from .data import CITIES
import random
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

ENEMY_GENERATORS = {
    "Desert Bandit": generate_bandit,
    "Mercenary": generate_mercenary,
    "Rival Trader": generate_rival_trader,
    "Nomad Warrior": generate_nomad_warrior,
    "Assassin": generate_assassin,
}
from  .actions.sell import handler_sell

class Action:
    id:str

"sell":handler_sell
handlers["sell"]

class Travel(Action):
    destination:str
def handle_travel(travel_action:Action):
    if not isinstance(travel_action, Travel):
        raise Exception
    ...
    travel_action.destination


def handle_action(action:Action, player, item_name=None, quantity=1, destination=None):
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

    handlers[action.id](player, action)
                        
    if actioa == "Buy":
        if item_name and item_name in CITIES[player["city"]]:
            base_price = CITIES[player["city"]][item_name]["buy"]
            trade_bonus = get_trade_bonus(player)

            final_unit_price = max(1, round(base_price * (1 - trade_bonus)))
            total_price = final_unit_price * quantity

            if player["gold"] >= total_price:
                player["gold"] -= total_price
                player["trade_inventory"][item_name] = player["trade_inventory"].get(item_name, 0) + quantity
                player["trade_xp"] += max(1, quantity)

                discount_percent = round(trade_bonus * 100, 1)
                message = (
                    f"Bought {quantity} {item_name}(s) for {total_price} gold "
                    f"({final_unit_price} each, {discount_percent}% trade bonus)."
                )
            else:
                message = f"Not enough gold to buy. You need {total_price} gold."
        else:
            message = "Invalid item to buy."

    elif action == "Sell":
        if item_name and player["trade_inventory"].get(item_name, 0) >= quantity:
            base_price = CITIES[player["city"]][item_name]["sell"]
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

        stats = compute_total_stats(player)
        fight_log = []

        player_hit_chance = stats.get("hit_chance", 75)
        player_dodge_chance = stats.get("dodge_chance", 0)
        player_damage_min = stats.get("damage_min", 1)
        player_damage_max = stats.get("damage_max", 2)
        player_strength = stats.get("strength", 5)
        player_armor = stats.get("armor", 0)

        # simple enemy defaults for now
       
        enemy_hit_chance = enemy.hit_chance
        enemy_dodge_chance = enemy.dodge_chance
        enemy_damage_min = enemy.damage_min
        enemy_damage_max = enemy.damage_max
        enemy_armor = enemy.armor

        while player["current_health"] > 0 and enemy.health > 0:
            # ----------------------------
            # PLAYER ATTACK
            # ----------------------------
            hit_roll = random.randint(1, 100)
            if hit_roll > player_hit_chance:
                fight_log.append(f"You miss the {enemy.name}!")
            else:
                dodge_roll = random.randint(1, 100)
                if dodge_roll <= enemy_dodge_chance:
                    fight_log.append(f"The {enemy.name} dodges your attack!")
                else:
                    raw_damage = random.randint(player_damage_min, player_damage_max) + player_strength
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

                fight_log.append(f"You earned {gold_reward} gold and {rep_reward} reputation.")

                # ----------------------------
                # ITEM DROP
                # ----------------------------
                luck = stats.get("luck", 0)
                drop_chance = 25 + luck * 2  # % chance

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

                        item_name = template["name"] if template else template_id

                        fight_log.append(f"You found: {item_name}!")
                        break
                else:
                    fight_log.append("No item dropped.")
                    break

            # ----------------------------
            # ENEMY ATTACK
            # ----------------------------
            enemy_hit_roll = random.randint(1, 100)
            if enemy_hit_roll > enemy_hit_chance:
                fight_log.append(f"The {enemy.name} misses you!")
            else:
                player_dodge_roll = random.randint(1, 100)
                if player_dodge_roll <= player_dodge_chance:
                    fight_log.append(f"You dodge the {enemy.name}'s attack!")
                else:
                    enemy_raw_damage = random.randint(enemy_damage_min, enemy_damage_max)
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

    else:
        message = "Unknown action."

    return message, player