import json
import os

PLAYER_FILE = "player.json"


class Player:
    def __init__(self, name):
        self.name = name
        self.city = "Baghdad"  # Starting city
        self.strength = 1
        self.intellect = 1
        self.agility = 1
        self.charisma = 1
        self.endurance = 1
        self.luck = 1
        self.current_health = self.max_health
        self.gold = 100
        self.reputation = 0
        self.inventory = {
            "Spices": 0,
            "Silk": 0,
            "Dates": 0,
            "Carpets": 0,
            "Incense": 0,
        }

    @property
    def max_health(self):
        return 50 + self.endurance * 1.2

    def train(self, skill):
        if skill == "strength":
            self.strength += 1
            print("You feel stronger!")
        elif skill == "intellect":
            self.intellect += 1
            print("You feel wiser!")
        elif skill == "agility":
            self.agility += 1
            print("You feel more stretchy")
        elif skill == "charisma":
            self.charisma += 1
            print("Others feel like you can, just because")
        elif skill == "endurance":
            self.endurance += 1
            print("You feel not as out of breath")
            # Update current_health if endurance changes
            self.current_health = min(self.current_health, self.max_health)
        elif skill == "luck":
            self.luck += 1
            print("You feel it will be a good day")
        else:
            print("Unknown skill.")

    def show_stats(self):
        print(f"\n{self.name} - Stats:")
        print(f"Health: {self.current_health}/{self.max_health}")
        print(f"Strength: {self.strength}")
        print(f"Intellect: {self.intellect}")
        print(f"Agility: {self.agility}")
        print(f"Charisma: {self.charisma}")
        print(f"Endurance: {self.endurance}")
        print(f"Luck: {self.luck}")
        print(f"Gold: {self.gold}")
        print(f"Reputation: {self.reputation}")
        print(f"Inventory: {self.inventory}\n")

    def to_dict(self):
        return {
            "name": self.name,
            "city": self.city,
            "current_health": self.current_health,
            "max_health": int(self.max_health),
            "strength": self.strength,
            "intellect": self.intellect,
            "agility": self.agility,
            "charisma": self.charisma,
            "endurance": self.endurance,
            "luck": self.luck,
            "gold": self.gold,
            "reputation": self.reputation,
            "inventory": self.inventory,
        }

    def save(self):
        with open(PLAYER_FILE, "w") as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load_from_dict(cls, data):
        player = cls(data["name"])
        # Use update but ensure current_health is set properly
        player.__dict__.update(data)
        # Just in case max_health changed due to endurance, clamp current_health:
        player.current_health = min(player.current_health, player.max_health)
        return player

    @classmethod
    def load(cls):
        if os.path.exists(PLAYER_FILE):
            with open(PLAYER_FILE, "r") as f:
                data = json.load(f)
            return cls.load_from_dict(data)
        else:
            return cls("Hero")
