# save.py

import json

def save_game(player, filename="savefile.json"):
    data = player.__dict__
    with open(filename, "w") as f:
        json.dump(data, f)
    print("Game saved.")

def load_game(filename="savefile.json"):
    from player import Player
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        player = Player(data["name"])
        player.__dict__.update(data)
        print("Game loaded.")
        return player
    except FileNotFoundError:
        print("No save file found.")
        return None
