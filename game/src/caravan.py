CAMEL_BUY_PRICE = 50
CAMEL_SELL_PRICE = 30
CAMEL_CAPACITY = 10  # units of cargo per camel


DEFAULT_CARAVAN = {
    "camels": 0,
    "cargo": {},  # {"Spices": 5, "Silk": 2, ...}
}


def get_caravan(player):
    if "caravan" not in player:
        player["caravan"] = {"camels": 0, "cargo": {}}

    if "cargo" not in player["caravan"]:
        player["caravan"]["cargo"] = {}

    return player["caravan"]


def caravan_capacity(player):
    caravan = get_caravan(player)
    return caravan["camels"] * CAMEL_CAPACITY


def caravan_cargo_total(player):
    caravan = get_caravan(player)
    return sum(caravan["cargo"].values())


def caravan_free_space(player):
    return caravan_capacity(player) - caravan_cargo_total(player)


def buy_camel(player, quantity=1):
    total_cost = CAMEL_BUY_PRICE * quantity

    if player["gold"] < total_cost:
        return (
            f"Not enough gold. You need {total_cost} gold to buy {quantity} camel(s)."
        )

    player["gold"] -= total_cost
    get_caravan(player)["camels"] += quantity

    return f"You bought {quantity} camel(s) for {total_cost} gold."


def sell_camel(player, quantity=1):
    caravan = get_caravan(player)

    if caravan["camels"] < quantity:
        return f"You don't have {quantity} camel(s) to sell."

    # Check if selling would leave cargo without capacity
    capacity_after = (caravan["camels"] - quantity) * CAMEL_CAPACITY
    cargo_total = caravan_cargo_total(player)

    if cargo_total > capacity_after:
        return (
            f"Cannot sell {quantity} camel(s) — your cargo ({cargo_total} units) "
            f"would exceed the remaining capacity ({capacity_after} units). "
            f"Unload some goods first."
        )

    total_earned = CAMEL_SELL_PRICE * quantity
    caravan["camels"] -= quantity
    player["gold"] += total_earned

    return f"You sold {quantity} camel(s) for {total_earned} gold."


def load_cargo(player, item_name, quantity=1):
    """Move goods from trade_inventory onto the caravan."""

    if item_name not in player.get("trade_inventory", {}):
        return "You don't have that item."

    in_inventory = player["trade_inventory"].get(item_name, 0)

    if in_inventory < quantity:
        return f"You only have {in_inventory} {item_name} in your pack."

    free = caravan_free_space(player)

    if free < quantity:
        return (
            f"Not enough caravan space. "
            f"Free capacity: {free} unit(s). Buy more camels to carry more."
        )

    player["trade_inventory"][item_name] -= quantity

    caravan = get_caravan(player)
    caravan["cargo"][item_name] = caravan["cargo"].get(item_name, 0) + quantity

    return f"Loaded {quantity} {item_name} onto the caravan."


def unload_cargo(player, item_name, quantity=1):
    """Move goods from the caravan back into trade_inventory."""

    caravan = get_caravan(player)
    on_caravan = caravan["cargo"].get(item_name, 0)

    if on_caravan < quantity:
        return f"The caravan only has {on_caravan} {item_name} loaded."

    caravan["cargo"][item_name] -= quantity

    if caravan["cargo"][item_name] == 0:
        del caravan["cargo"][item_name]

    player["trade_inventory"][item_name] = (
        player["trade_inventory"].get(item_name, 0) + quantity
    )

    return f"Unloaded {quantity} {item_name} from the caravan."
