from player import Player
from location import show_locations, enter_location
from save import save_game, load_game

def main():
    print("Welcome to Desert Kingdoms RPG!")
    choice = input("Load game? (y/n): ").lower()
    if choice == "y":
        player = load_game()
        if not player:
            name = input("Enter your name: ")
            player = Player(name)
    else:
        name = input("Enter your name: ")
        player = Player(name)

    while True:
        print("\n--- Main Menu ---")
        print("1. Travel")
        print("2. View Stats")
        print("3. Save Game")
        print("4. Exit")

        choice = input("> ")
        if choice == "1":
            show_locations()
            loc = input("Choose a location: ")
            enter_location(loc, player)
        elif choice == "2":
            player.show_stats()
        elif choice == "3":
            save_game(player)
        elif choice == "4":
            print("Farewell.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
