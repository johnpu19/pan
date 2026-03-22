import json
import os
from items import get_template

PLAYER_FILE = 'data/player.json'


class Player:
    def __init__(self, name):
        self.name = name
        self.city = "Baghdad"

        # base stats
        self.health = 100
        self.strength = 5
        self.intellect = 5

        self.gold = 100
        self.reputation = 0

        # trade goods
        self.trade_inventory = {
            "Spices": 0,
            "Silk": 0,
            "Dates": 0,
            "Carpets": 0,
            "Incense": 0,
        }

        # item system
        self.owned_items = {}      # instance_id -> item dict
        self.inventory_ids = []    # unequipped item ids
        self.equipment = {
            "weapon": None,
            "head": None,
            "chest": None,
            "ring_1": None,
            "ring_2": None,
        }

    def train(self, skill):
        if skill == "strength":
            self.strength += 1
            print("You feel stronger!")
        elif skill == "intellect":
            self.intellect += 1
            print("You feel wiser!")
        else:
            print("Unknown skill.")

    def get_total_stats(self):
        total_strength = self.strength
        total_intellect = self.intellect

        for slot, instance_id in self.equipment.items():
            if instance_id is None:
                continue

            item = self.owned_items.get(instance_id)
            if item is None:
                continue

            template = get_template(item["template_id"])
            if template is None:
                continue

            base_stats = template.get("base_stats", {})
            bonus_stats = item.get("bonus_stats", {})

            total_strength += base_stats.get("strength", 0)
            total_strength += bonus_stats.get("strength", 0)

            total_intellect += base_stats.get("intellect", 0)
            total_intellect += bonus_stats.get("intellect", 0)

        return {
            "health": self.health,
            "strength": total_strength,
            "intellect": total_intellect,
            "gold": self.gold,
            "reputation": self.reputation,
        }
    
    def show_stats(self):
        total = self.get_total_stats()

        print(f"\n{self.name} - Stats:")
        print(f"Health: {total['health']}")
        print(f"Strength: {total['strength']} (base: {self.strength})")
        print(f"Intellect: {total['intellect']} (base: {self.intellect})")
        print(f"Gold: {total['gold']}")
        print(f"Reputation: {total['reputation']}")

        print("\nTrade goods:")
        print(self.trade_inventory)

        print("\nEquipped:")
        for slot, instance_id in self.equipment.items():
            if instance_id is None:
                print(f"{slot}: None")
            else:
                item = self.owned_items.get(instance_id)
                if item:
                    template = get_template(item["template_id"])
                    item_name = template["name"] if template else "Unknown Item"
                    print(f"{slot}: {item_name}")
                else:
                    print(f"{slot}: Broken item reference")

        print("\nInventory:")
        if not self.inventory_ids:
            print("Empty")
        else:
            for instance_id in self.inventory_ids:
                item = self.owned_items.get(instance_id)
                if item:
                    template = get_template(item["template_id"])
                    item_name = template["name"] if template else "Unknown Item"
                    print(f"- {item_name} ({instance_id[:8]})")
                else:
                    print(f"- Broken item reference ({instance_id})")

        print()

   

    def to_dict(self):
        return {
            'name': self.name,
            'city': self.city,
            'health': self.health,
            'strength': self.strength,
            'intellect': self.intellect,
            'gold': self.gold,
            'reputation': self.reputation,
            'trade_inventory': self.trade_inventory,
            'owned_items': self.owned_items,
            'inventory_ids': self.inventory_ids,
            'equipment': self.equipment,
        }

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(PLAYER_FILE, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load(cls):
        if os.path.exists(PLAYER_FILE):
            with open(PLAYER_FILE, 'r') as f:
                data = json.load(f)

            player = cls(data['name'])
            player.city = data['city']
            player.health = data['health']
            player.strength = data['strength']
            player.intellect = data['intellect']
            player.gold = data['gold']
            player.reputation = data['reputation']
            player.trade_inventory = data.get('trade_inventory', {})
            player.owned_items = data.get('owned_items', {})
            player.inventory_ids = data.get('inventory_ids', [])
            player.equipment = data.get('equipment', {
                "weapon": None,
                "head": None,
                "chest": None,
                "ring_1": None,
                "ring_2": None,
            })

            return player
        else:
            return cls("Hero")