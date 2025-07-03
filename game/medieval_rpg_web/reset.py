import os

if os.path.exists("player.json"):
    os.remove("player.json")
    print("player.json deleted.")
else:
    print("player.json does not exist.")