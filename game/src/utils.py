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

def get_trade_bonus(player):
    base_stats = player.get("base_stats", {})
    intellect = base_stats.get("intellect", 0)
    reputation = player.get("reputation", 0)
    trade_xp = player.get("trade_xp", 0)

    intellect_bonus = intellect * 0.005          # 0.5% per point
    reputation_bonus = reputation * 0.003        # 0.3% per point
    trade_xp_bonus = (trade_xp // 10) * 0.002    # 0.2% per 10 XP

    total_bonus = intellect_bonus + reputation_bonus + trade_xp_bonus

    return min(total_bonus, 0.30)  # cap at 30%