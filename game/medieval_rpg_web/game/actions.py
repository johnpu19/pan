# game/actions.py
from game.data import CITIES

def process_action(action, player, item_name=None, quantity=1):
    city = player['city']
    market = CITIES[city]
    message = ""

    if action == 'Buy':
        price = market.get(item_name, {}).get('buy')
        if price and player['gold'] >= price * quantity:
            player['gold'] -= price * quantity
            player['inventory'][item_name] = player['inventory'].get(item_name, 0) + quantity
            message = f"Bought {quantity} {item_name}(s) for {price * quantity} gold."
        else:
            message = f"Cannot buy {item_name}."

    elif action == 'Sell':
        price = market.get(item_name, {}).get('sell')
        if price and player['inventory'].get(item_name, 0) >= quantity:
            player['gold'] += price * quantity
            player['inventory'][item_name] -= quantity
            message = f"Sold {quantity} {item_name}(s) for {price * quantity} gold."
        else:
            message = f"Cannot sell {item_name}."

    elif action == 'Travel':
        destination = item_name
        if destination in CITIES:
            player['city'] = destination
            message = f"You traveled to {destination}."
        else:
            message = "Unknown destination."

    elif action == 'Train':
        player['strength'] += 1
        message = "You trained and gained 1 strength."

    elif action == 'Rest':
        player['health'] = 100
        message = "You rested and fully restored your health."

    elif action == 'Fight':
        player['health'] -= 10
        player['gold'] += 5
        message = "You fought bravely. -10 health, +5 gold."

    else:
        message = "Unknown action."

    return message, player

