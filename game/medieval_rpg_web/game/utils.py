from .items import get_template
from .stats import merge_stats, derive_stats_from_base

def get_equipment_bonus_stats(player):
    bonus = {}

    equipment = player.get("equipment", {})
    owned_items = player.get("owned_items", {})

    for slot, instance_id in equipment.items():
        if not instance_id:
            continue

        item = owned_items.get(instance_id)
        if not item:
            continue

        template = get_template(item["template_id"])
        if not template:
            continue

        for source in [template.get("base_stats", {}), item.get("bonus_stats", {})]:
            for stat, value in source.items():
                bonus[stat] = bonus.get(stat, 0) + value

    return bonus

def compute_total_stats(player):
    base_stats = player.get("base_stats", {})
    derived_stats = derive_stats_from_base(base_stats)
    starting_total = merge_stats(base_stats, derived_stats)

    equipment_bonus = get_equipment_bonus_stats(player)
    total = merge_stats(starting_total, equipment_bonus)

    return total