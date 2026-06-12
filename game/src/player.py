import json
import os
from copy import deepcopy

from .stats import DEFAULT_BASE_STATS
from .items import get_template


PLAYER_FILE = "data/player.json"


DEFAULT_TRAVEL = {
    "active": False,
    "from": None,
    "to": None,
    "progress": 0,
    "distance": 0,
    "danger": 0,
    "route_name": None,
}


DEFAULT_TRADE_INVENTORY = {
    "Spices": 0,
    "Silk": 0,
    "Dates": 0,
    "Carpets": 0,
    "Incense": 0,
}


DEFAULT_EQUIPMENT = {
    "weapon": None,
    "head": None,
    "chest": None,
    "ring_1": None,
    "ring_2": None,
}


DEFAULT_CARAVAN = {
    "camels": 0,
    "cargo": {},
}


def get_max_health(base_stats):
    return 50 + base_stats.get("vitality", 5) * 10


def create_new_player(name="Traveler"):
    """
    Creates a clean dictionary version of a new player.
    This is useful for Flask sessions.
    """
    return Player(name).to_dict()


def normalize_player_dict(data):
    """
    Safety net for old saves / old session data.

    This keeps the game from crashing if you add new fields later.
    """
    if data is None:
        data = {}

    # Old versions used direct stats like strength/intellect.
    base_stats = deepcopy(DEFAULT_BASE_STATS)
    base_stats.update(data.get("base_stats", {}))

    if "strength" in data:
        base_stats["strength"] = data.get("strength", base_stats["strength"])

    if "intellect" in data:
        base_stats["intellect"] = data.get("intellect", base_stats["intellect"])

    trade_inventory = deepcopy(DEFAULT_TRADE_INVENTORY)
    trade_inventory.update(data.get("trade_inventory", {}))

    equipment = deepcopy(DEFAULT_EQUIPMENT)
    equipment.update(data.get("equipment", {}))

    travel = deepcopy(DEFAULT_TRAVEL)
    travel.update(data.get("travel", {}))

    caravan = deepcopy(DEFAULT_CARAVAN)
    caravan.update(data.get("caravan", {}))

    if "cargo" not in caravan or caravan["cargo"] is None:
        caravan["cargo"] = {}

    city = data.get("city", "baghdad")
    if isinstance(city, str):
        city = city.lower()
    else:
        city = "baghdad"

    current_health = data.get("current_health")

    # Very old saves may have used "health" instead of "current_health".
    if current_health is None:
        current_health = data.get("health", get_max_health(base_stats))

    max_health = get_max_health(base_stats)
    current_health = max(1, min(current_health, max_health))

    return {
        "name": data.get("name", "Traveler"),
        "city": city,

        "gold": data.get("gold", 100),
        "reputation": data.get("reputation", 0),

        "level": data.get("level", 1),
        "xp": data.get("xp", 0),
        "trade_xp": data.get("trade_xp", 0),

        "base_stats": base_stats,
        "current_health": current_health,

        "trade_inventory": trade_inventory,

        "owned_items": data.get("owned_items", {}),
        "inventory_ids": data.get("inventory_ids", []),
        "equipment": equipment,

        "caravan": caravan,
        "travel": travel,
    }


class Player:
    def __init__(self, name):
        self.name = name
        self.city = "baghdad"

        self.gold = 100
        self.reputation = 0

        self.level = 1
        self.xp = 0
        self.trade_xp = 0

        self.base_stats = deepcopy(DEFAULT_BASE_STATS)
        self.current_health = get_max_health(self.base_stats)

        self.trade_inventory = deepcopy(DEFAULT_TRADE_INVENTORY)

        self.owned_items = {}
        self.inventory_ids = []
        self.equipment = deepcopy(DEFAULT_EQUIPMENT)

        self.caravan = deepcopy(DEFAULT_CARAVAN)
        self.travel = deepcopy(DEFAULT_TRAVEL)

    def train(self, skill):
        if skill not in self.base_stats:
            print("Unknown skill.")
            return

        old_max_health = get_max_health(self.base_stats)

        self.base_stats[skill] += 1

        new_max_health = get_max_health(self.base_stats)

        # If vitality increases, preserve the same missing-health amount.
        if skill == "vitality":
            gained_max_health = new_max_health - old_max_health
            self.current_health += gained_max_health

        print(f"You improved your {skill}!")

    def get_total_stats(self):
        total_stats = deepcopy(self.base_stats)

        for slot, instance_id in self.equipment.items():
            if instance_id is None:
                continue

            item = self.owned_items.get(instance_id)
            if item is None:
                continue

            template = get_template(item["template_id"])
            if template is None:
                continue

            template_stats = template.get("base_stats", {})
            bonus_stats = item.get("bonus_stats", {})

            for stat_name, value in template_stats.items():
                total_stats[stat_name] = total_stats.get(stat_name, 0) + value

            for stat_name, value in bonus_stats.items():
                total_stats[stat_name] = total_stats.get(stat_name, 0) + value

        max_health = get_max_health(total_stats)

        return {
            "current_health": self.current_health,
            "max_health": max_health,
            "base_stats": self.base_stats,
            "total_stats": total_stats,

            "gold": self.gold,
            "reputation": self.reputation,

            "level": self.level,
            "xp": self.xp,
            "trade_xp": self.trade_xp,
        }

    def show_stats(self):
        total = self.get_total_stats()

        print(f"\n{self.name} - Stats:")
        print(f"Level: {total['level']}")
        print(f"XP: {total['xp']}")
        print(f"Trade XP: {total['trade_xp']}")
        print(f"Health: {total['current_health']} / {total['max_health']}")
        print(f"Gold: {total['gold']}")
        print(f"Reputation: {total['reputation']}")

        print("\nAttributes:")
        for stat_name, total_value in total["total_stats"].items():
            base_value = total["base_stats"].get(stat_name, 0)
            print(f"{stat_name.title()}: {total_value} (base: {base_value})")

        print("\nTrade goods:")
        print(self.trade_inventory)

        print("\nCaravan:")
        print(f"Camels: {self.caravan.get('camels', 0)}")
        print(f"Cargo: {self.caravan.get('cargo', {})}")

        print("\nEquipped:")
        for slot, instance_id in self.equipment.items():
            if instance_id is None:
                print(f"{slot}: None")
                continue

            item = self.owned_items.get(instance_id)
            if item is None:
                print(f"{slot}: Broken item reference")
                continue

            template = get_template(item["template_id"])
            item_name = template["name"] if template else "Unknown Item"
            print(f"{slot}: {item_name}")

        print("\nInventory:")
        if not self.inventory_ids:
            print("Empty")
        else:
            for instance_id in self.inventory_ids:
                item = self.owned_items.get(instance_id)

                if item is None:
                    print(f"- Broken item reference ({instance_id})")
                    continue

                template = get_template(item["template_id"])
                item_name = template["name"] if template else "Unknown Item"
                print(f"- {item_name} ({instance_id[:8]})")

        print()

    def to_dict(self):
        return normalize_player_dict({
            "name": self.name,
            "city": self.city,

            "gold": self.gold,
            "reputation": self.reputation,

            "level": self.level,
            "xp": self.xp,
            "trade_xp": self.trade_xp,

            "base_stats": self.base_stats,
            "current_health": self.current_health,

            "trade_inventory": self.trade_inventory,

            "owned_items": self.owned_items,
            "inventory_ids": self.inventory_ids,
            "equipment": self.equipment,

            "caravan": self.caravan,
            "travel": self.travel,
        })

    def save(self):
        os.makedirs("data", exist_ok=True)

        with open(PLAYER_FILE, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def from_dict(cls, data):
        data = normalize_player_dict(data)

        player = cls(data["name"])

        player.city = data["city"]

        player.gold = data["gold"]
        player.reputation = data["reputation"]

        player.level = data["level"]
        player.xp = data["xp"]
        player.trade_xp = data["trade_xp"]

        player.base_stats = data["base_stats"]
        player.current_health = data["current_health"]

        player.trade_inventory = data["trade_inventory"]

        player.owned_items = data["owned_items"]
        player.inventory_ids = data["inventory_ids"]
        player.equipment = data["equipment"]

        player.caravan = data["caravan"]
        player.travel = data["travel"]

        return player

    @classmethod
    def load(cls):
        if not os.path.exists(PLAYER_FILE):
            return cls("Traveler")

        with open(PLAYER_FILE, "r") as f:
            data = json.load(f)

        return cls.from_dict(data)