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