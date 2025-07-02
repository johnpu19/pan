# enemies.py

import random

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

def generate_bandit():
    return Enemy("Desert Bandit", health=random.randint(30, 60), attack=random.randint(5, 10))

def generate_mercenary():
    return Enemy("Mercenary", health=random.randint(50, 80), attack=random.randint(8, 14))

def generate_rival_trader():
    return Enemy("Rival Trader", health=random.randint(40, 70), attack=random.randint(6, 12))

def generate_nomad_warrior():
    return Enemy("Nomad Warrior", health=random.randint(45, 75), attack=random.randint(7, 13))

def generate_assassin():
    return Enemy("Assassin", health=random.randint(35, 60), attack=random.randint(10, 15))
