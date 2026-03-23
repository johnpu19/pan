from .items import get_template


def equip_item(player, instance_id):
    item = player["owned_items"].get(instance_id)
    if item is None:
        return False, "Item does not exist."

    if instance_id not in player["inventory_ids"]:
        return False, "Item is not in inventory."

    template = get_template(item["template_id"])
    if template is None:
        return False, "Item template not found."

    equip_slot = template.get("equip_slot")
    if equip_slot is None:
        return False, "This item cannot be equipped."

    # special handling for rings
    if equip_slot == "ring":
        if player["equipment"].get("ring_1") is None:
            target_slot = "ring_1"
        elif player["equipment"].get("ring_2") is None:
            target_slot = "ring_2"
        else:
            return False, "Both ring slots are full."
    else:
        target_slot = equip_slot

    if target_slot not in player["equipment"]:
        return False, f"Invalid equipment slot: {target_slot}"

    old_item_id = player["equipment"][target_slot]

    player["inventory_ids"].remove(instance_id)
    player["equipment"][target_slot] = instance_id

    if old_item_id is not None:
        player["inventory_ids"].append(old_item_id)

    return True, f"Equipped {template['name']} in slot: {target_slot}"

def unequip_item(player, slot):
    if slot not in player["equipment"]:
        return False, "Invalid slot."

    instance_id = player["equipment"][slot]
    if instance_id is None:
        return False, "Nothing equipped there."

    player["equipment"][slot] = None
    player["inventory_ids"].append(instance_id)

    item = player["owned_items"].get(instance_id)
    if item is None:
        return True, "Unequipped item."

    template = get_template(item["template_id"])
    item_name = template["name"] if template else "Unknown Item"
    return True, f"Unequipped {item_name} from {slot}"

def find_item_location(player, instance_id):
    if instance_id in player["inventory_ids"]:
        return "inventory"

    for slot, equipped_id in player["equipment"].items():
        if equipped_id == instance_id:
            return slot

    return None


def sell_item(player, instance_id):
    item = player["owned_items"].get(instance_id)
    if item is None:
        return False, "Item does not exist."

    template = get_template(item["template_id"])
    if template is None:
        return False, "Item template not found."

    location = find_item_location(player, instance_id)
    if location is None:
        return False, "Item is not owned properly."

    if location == "inventory":
        player["inventory_ids"].remove(instance_id)
    else:
        player["equipment"][location] = None

    sell_price = max(1, template.get("value", 0) // 2)
    player["gold"] += sell_price

    del player["owned_items"][instance_id]

    return True, f"Sold {template['name']} for {sell_price} gold."


def drop_item(player, instance_id):
    item = player["owned_items"].get(instance_id)
    if item is None:
        return False, "Item does not exist."

    template = get_template(item["template_id"])
    item_name = template["name"] if template else "Unknown Item"

    location = find_item_location(player, instance_id)
    if location is None:
        return False, "Item is not owned properly."

    if location == "inventory":
        player["inventory_ids"].remove(instance_id)
    else:
        player["equipment"][location] = None

    del player["owned_items"][instance_id]

    return True, f"Dropped {item_name}."