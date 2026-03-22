from player import Player
from inventory_service import unequip_item

player = Player.load()

print("\nBEFORE UNEQUIP")
player.show_stats()

unequip_item(player, "weapon")

print("\nAFTER UNEQUIP")
player.show_stats()

player.save()
print("Player saved.")