DEFAULT_BASE_STATS = {
    "strength": 5,
    "agility": 5,
    "vitality": 5,
    "intellect": 5,
    "luck": 3,
}

def merge_stats(base, bonus):
    total = dict(base)
    for stat, value in bonus.items():
        total[stat] = total.get(stat, 0) + value
    return total

def derive_stats_from_base(base_stats):
    vitality = base_stats.get("vitality", 0)
    agility = base_stats.get("agility", 0)

    return {
        "max_health": 50 + vitality * 10,
        "damage_min": 1,
        "damage_max": 2,
        "armor": 0,
        "hit_chance": min(75 + agility * 2, 95),
        "dodge_chance": min(int(agility * 1.5), 50),
    }