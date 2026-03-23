class Enemy:
    def __init__(
        self,
        name,
        max_health,
        damage_min,
        damage_max,
        armor=0,
        hit_chance=80,
        dodge_chance=5,
        gold_min=15,
        gold_max=40,
        rep_min=1,
        rep_max=5,
    ):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.damage_min = damage_min
        self.damage_max = damage_max
        self.armor = armor
        self.hit_chance = hit_chance
        self.dodge_chance = dodge_chance
        self.gold_min = gold_min
        self.gold_max = gold_max
        self.rep_min = rep_min
        self.rep_max = rep_max


def generate_bandit():
    return Enemy(
        name="Desert Bandit",
        max_health=35,
        damage_min=3,
        damage_max=6,
        armor=0,
        hit_chance=78,
        dodge_chance=8,
        gold_min=10,
        gold_max=25,
        rep_min=1,
        rep_max=3,
    )


def generate_mercenary():
    return Enemy(
        name="Mercenary",
        max_health=50,
        damage_min=5,
        damage_max=8,
        armor=20,
        hit_chance=82,
        dodge_chance=5,
        gold_min=20,
        gold_max=40,
        rep_min=2,
        rep_max=4,
    )


def generate_rival_trader():
    return Enemy(
        name="Rival Trader",
        max_health=30,
        damage_min=2,
        damage_max=5,
        armor=0,
        hit_chance=75,
        dodge_chance=4,
        gold_min=25,
        gold_max=50,
        rep_min=1,
        rep_max=2,
    )


def generate_nomad_warrior():
    return Enemy(
        name="Nomad Warrior",
        max_health=45,
        damage_min=4,
        damage_max=7,
        armor=1,
        hit_chance=80,
        dodge_chance=7,
        gold_min=18,
        gold_max=35,
        rep_min=2,
        rep_max=4,
    )


def generate_assassin():
    return Enemy(
        name="Assassin",
        max_health=28,
        damage_min=6,
        damage_max=10,
        armor=0,
        hit_chance=88,
        dodge_chance=15,
        gold_min=30,
        gold_max=60,
        rep_min=3,
        rep_max=6,
    )

LOOT_TABLES = {
    "Desert Bandit": ["rusty_dagger", "iron_scimitar", "copper_ring"],
    "Mercenary": ["leather_vest", "chain_shirt", "steel_saber"],
    "Rival Trader": ["silver_ring", "golden_ring"],
    "Nomad Warrior": ["iron_scimitar", "leather_vest", "chain_shirt"],
    "Assassin": ["rusty_dagger", "leather_hood", "golden_ring"],
}