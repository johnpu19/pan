import json
import os

PLAYER_FILE = 'player.json'

class Player:
    def __init__(self, name):
        self.name = name
        self.city = "Baghdad"  # Starting city
        self.health = 100
        self.strength = 5
        self.intellect = 5
        self.gold = 100
        self.reputation = 0
        self.inventory = {
            "Spices": 0,
            "Silk": 0,
            "Dates": 0,
            "Carpets": 0,
            "Incense": 0,
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

    def show_stats(self):
        print(f"\n{self.name} - Stats:")
        print(f"Health: {self.health}")
        print(f"Strength: {self.strength}")
        print(f"Intellect: {self.intellect}")
        print(f"Gold: {self.gold}")
        print(f"Reputation: {self.reputation}")
        print(f"Inventory: {self.inventory}\n")

    def to_dict(self):
        return {
            'name': self.name,
            'city': self.city,
            'health': self.health,
            'strength': self.strength,
            'intellect': self.intellect,
            'gold': self.gold,
            'reputation': self.reputation,
            'inventory': self.inventory,
        }

    def save(self):
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
            player.inventory = data['inventory']
            return player
        else:
            # Return new player with default values
            return cls("Hero")
