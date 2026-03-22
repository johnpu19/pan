from items import get_template


def equip_item(player, instance_id):
    # item must exist
    item = player.owned_items.get(instance_id)
    if item is None:
        print("Item does not exist.")
        return False

    # item must currently be in inventory
    if instance_id not in player.inventory_ids:
        print("Item is not in inventory.")
        return False

    template = get_template(item["template_id"])
    if template is None:
        print("Item template not found.")
        return False

    equip_slot = template.get("equip_slot")
    if equip_slot is None:
        print("This item cannot be equipped.")
        return False

    # handle special slots like rings later
    target_slot = equip_slot

    if target_slot not in player.equipment:
        print(f"Invalid equipment slot: {target_slot}")
        return False

    # swap out old item if something is already equipped
    old_item_id = player.equipment[target_slot]

    # remove new item from inventory
    player.inventory_ids.remove(instance_id)

    # equip new item
    player.equipment[target_slot] = instance_id

    # old equipped item goes back to inventory
    if old_item_id is not None:
        player.inventory_ids.append(old_item_id)

    print(f"Equipped {template['name']} in slot: {target_slot}")
    return True


def unequip_item(player, slot):
    if slot not in player.equipment:
        print("Invalid slot.")
        return False

    instance_id = player.equipment[slot]
    if instance_id is None:
        print("Nothing equipped there.")
        return False

    player.equipment[slot] = None
    player.inventory_ids.append(instance_id)

    item = player.owned_items[instance_id]
    template = get_template(item["template_id"])
    print(f"Unequipped {template['name']} from {slot}")
    return True


