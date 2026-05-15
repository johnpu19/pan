import uuid

ITEM_TEMPLATES = {
    "iron_scimitar": {
    "template_id": "iron_scimitar",
    "name": "Iron Scimitar",
    "category": "weapon",
    "equip_slot": "weapon",
    "value": 60,
    "base_stats": {
        "damage_min": 3,
        "damage_max": 5,
        "strength": 1
    },
    "icon": "icons/iron_scimitar.png",
    "rarity": "common",
    "stackable": False,
},

"rusty_dagger": {
    "template_id": "rusty_dagger",
    "name": "Rusty Dagger",
    "category": "weapon",
    "equip_slot": "weapon",
    "value": 20,
    "base_stats": {
        "damage_min": 1,
        "damage_max": 3,
        "agility": 1
    },
    "icon": "icons/rusty_dagger.png",
    "rarity": "common",
    "stackable": False,
},

"steel_saber": {
    "template_id": "steel_saber",
    "name": "Steel Saber",
    "category": "weapon",
    "equip_slot": "weapon",
    "value": 100,
    "base_stats": {
        "damage_min": 5,
        "damage_max": 8,
        "strength": 2
    },
    "icon": "icons/steel_saber.png",
    "rarity": "uncommon",
    "stackable": False,
},

"leather_vest": {
    "template_id": "leather_vest",
    "name": "Leather Vest",
    "category": "armor",
    "equip_slot": "chest",
    "value": 50,
    "base_stats": {
        "armor": 2,
        "vitality": 1
    },
    "icon": "icons/leather_vest.png",
    "rarity": "common",
    "stackable": False,
},

"cloth_robe": {
    "template_id": "cloth_robe",
    "name": "Cloth Robe",
    "category": "armor",
    "equip_slot": "chest",
    "value": 25,
    "base_stats": {
        "intellect": 2
    },
    "icon": "icons/cloth_robe.png",
    "rarity": "common",
    "stackable": False,
},

"chain_shirt": {
    "template_id": "chain_shirt",
    "name": "Chain Shirt",
    "category": "armor",
    "equip_slot": "chest",
    "value": 80,
    "base_stats": {
        "armor": 3,
        "vitality": 1
    },
    "icon": "icons/chain_shirt.png",
    "rarity": "uncommon",
    "stackable": False,
},

"copper_ring": {
    "template_id": "copper_ring",
    "name": "Copper Ring",
    "category": "accessory",
    "equip_slot": "ring",
    "value": 30,
    "base_stats": {
        "agility": 1
    },
    "icon": "icons/copper_ring.png",
    "rarity": "common",
    "stackable": True,
},

"silver_ring": {
    "template_id": "silver_ring",
    "name": "Silver Ring",
    "category": "accessory",
    "equip_slot": "ring",
    "value": 50,
    "base_stats": {
        "intellect": 2
    },
    "icon": "icons/silver_ring.png",
    "rarity": "common",
    "stackable": False,
},

"golden_ring": {
    "template_id": "golden_ring",
    "name": "Golden Ring",
    "category": "accessory",
    "equip_slot": "ring",
    "value": 90,
    "base_stats": {
        "luck": 2
    },
    "icon": "icons/golden_ring.png",
    "rarity": "uncommon",
    "stackable": False,
},

"leather_hood": {
    "template_id": "leather_hood",
    "name": "Leather Hood",
    "category": "armor",
    "equip_slot": "head",
    "value": 40,
    "base_stats": {
        "agility": 2
    },
    "icon": "icons/leather_hood.png",
    "rarity": "common",
    "stackable": False,
},

"scholar_turban": {
    "template_id": "scholar_turban",
    "name": "Scholar's Turban",
    "category": "armor",
    "equip_slot": "head",
    "value": 60,
    "base_stats": {
        "intellect": 3
    },
    "icon": "icons/scholar_turban.png",
    "rarity": "uncommon",
    "stackable": False,
},

"nomad_spear": {
    "template_id": "nomad_spear",
    "name": "Nomad Spear",
    "category": "weapon",
    "equip_slot": "weapon",
    "value": 70,
    "base_stats": {
        "damage_min": 4,
        "damage_max": 6,
        "agility": 1,
        "strength": 1
    },
    "icon": "icons/nomad_spear.png",
    "rarity": "common",
    "stackable": False,
},

"merchants_coat": {
    "template_id": "merchants_coat",
    "name": "Merchant's Coat",
    "category": "armor",
    "equip_slot": "chest",
    "value": 65,
    "base_stats": {
        "intellect": 1,
        "luck": 1
    },
    "icon": "icons/merchants_coat.png",
    "rarity": "common",
    "stackable": False,
},

"iron_helm": {
    "template_id": "iron_helm",
    "name": "Iron Helm",
    "category": "armor",
    "equip_slot": "head",
    "value": 55,
    "base_stats": {
        "armor": 2,
        "vitality": 1
    },
    "icon": "icons/iron_helm.png",
    "rarity": "common",
    "stackable": False,
},

"nomad_wrap": {
    "template_id": "nomad_wrap",
    "name": "Nomad Wrap",
    "category": "armor",
    "equip_slot": "head",
    "value": 45,
    "base_stats": {
        "agility": 1,
        "luck": 1
    },
    "icon": "icons/nomad_wrap.png",
    "rarity": "common",
    "stackable": False,
},

"warriors_ring": {
    "template_id": "warriors_ring",
    "name": "Warrior's Ring",
    "category": "accessory",
    "equip_slot": "ring",
    "value": 60,
    "base_stats": {
        "strength": 1
    },
    "icon": "icons/warriors_ring.png",
    "rarity": "common",
    "stackable": False,
},

"guards_ring": {
    "template_id": "guards_ring",
    "name": "Guard's Ring",
    "category": "accessory",
    "equip_slot": "ring",
    "value": 60,
    "base_stats": {
        "vitality": 1
    },
    "icon": "icons/guards_ring.png",
    "rarity": "common",
    "stackable": False,
},

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