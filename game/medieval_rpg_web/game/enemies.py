# enemies.py

import random

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

def generate_bandit():
    return Enemy("Desert Bandit", health=random.randint(30, 60), attack=random.randint(5, 10))
