import uuid

ITEM_TEMPLATES = {
    "iron_scimitar": {
        "template_id": "iron_scimitar",
        "name": "Iron Scimitar",
        "category": "weapon",
        "equip_slot": "weapon",
        "value": 60,
        "base_stats": {
            "strength": 2
        },
        "icon": "icons/iron_scimitar.png",
        "rarity": "common",
        "stackable": False,
    }
}


def create_item_instance(template_id, quantity=1):
    if template_id not in ITEM_TEMPLATES:
        raise ValueError(f"Unknown template_id: {template_id}")

    return {
        "instance_id": str(uuid.uuid4()),
        "template_id": template_id,
        "quantity": quantity,
        "bonus_stats": {},
        "durability": None,
    }


def get_template(template_id):
    return ITEM_TEMPLATES.get(template_id)