# location.py

def show_locations():
    print("\nYou can travel to:")
    print("1. Bazaar")
    print("2. Training Grounds")
    print("3. Desert")
    print("4. Palace")
    print("5. Back")
    
def enter_location(choice, player):
    if choice == "1":
        print("You arrive at the bustling Bazaar full of merchants.")
        from actions import trade
        trade(player)
    elif choice == "2":
        print("You head to the Training Grounds.")
        skill = input("Train strength or intellect? > ")
        player.train(skill)
    elif choice == "3":
        print("You ride out into the Desert...")
        from actions import fight
        fight(player)
    elif choice == "4":
        print("You visit the Palace of the Sultan. Reputation matters here.")
        if player.reputation >= 10:
            print("The guards bow and let you enter. You gain favor.")
            player.gold += 50
        else:
            print("The guards ignore you. You need more reputation.")
    elif choice == "5":
        return
    else:
        print("Invalid choice.")
