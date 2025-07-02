# actions.py

from items import goods

def trade(player):
    while True:
        print("\nBazaar Options:")
        print("1. Buy")
        print("2. Sell")
        print("3. Leave Bazaar")
        choice = input("> ")

        if choice == "1":
            print("\nGoods for Sale:")
            for item, price in goods.items():
                print(f"{item.title()} - {price['buy_price']} gold")
            item = input("What do you want to buy? > ").lower()
            if item in goods and player.gold >= goods[item]["buy_price"]:
                player.gold -= goods[item]["buy_price"]
                player.inventory.append(item)
                print(f"You bought 1 {item}.")
            else:
                print("Invalid item or insufficient gold.")
        elif choice == "2":
            print("\nYour Inventory:")
            for i, item in enumerate(player.inventory, 1):
                print(f"{i}. {item}")
            item = input("What do you want to sell? > ").lower()
            if item in player.inventory:
                player.gold += goods.get(item, {"sell_price": 0})["sell_price"]
                player.inventory.remove(item)
                print(f"You sold 1 {item}.")
            else:
                print("You don't have that item.")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
from enemies import generate_bandit
import random

def fight(player):
    enemy = generate_bandit()
    print(f"\nA wild {enemy.name} appears! Combat begins.")

    while player.health > 0 and enemy.health > 0:
        print(f"\nYour HP: {player.health} | {enemy.name} HP: {enemy.health}")
        move = input("Attack or Run? > ").lower()
        if move == "attack":
            damage = random.randint(player.strength, player.strength + 5)
            enemy.health -= damage
            print(f"You hit the {enemy.name} for {damage} damage.")

            if enemy.health > 0:
                edamage = random.randint(enemy.attack - 2, enemy.attack + 2)
                player.health -= edamage
                print(f"{enemy.name} hits you for {edamage} damage.")
        elif move == "run":
            print("You fled the battle.")
            return
        else:
            print("Invalid move.")

    if player.health <= 0:
        print("You have fallen in battle... Game Over.")
        exit()
    else:
        print(f"You defeated the {enemy.name}!")
        gold_reward = random.randint(10, 50)
        rep_gain = random.randint(1, 5)
        player.gold += gold_reward
        player.reputation += rep_gain
        print(f"You looted {gold_reward} gold and earned {rep_gain} reputation.")

