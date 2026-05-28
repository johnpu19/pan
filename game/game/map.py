MAP = {
    "damascus": {
        "name": "Damascus",
        "description": "Ancient city of scholars, markets, and gardens.",
        "connections": {
            "aleppo": {
                "distance": 3,
                "danger": 2,
                "route_name": "Northern caravan road",
            },
            "baghdad": {
                "distance": 5,
                "danger": 3,
                "route_name": "Eastern desert road",
            },
        },
    },

    "aleppo": {
        "name": "Aleppo",
        "description": "A trade hub famous for soap, textiles, and guarded warehouses.",
        "connections": {
            "damascus": {
                "distance": 3,
                "danger": 2,
                "route_name": "Southern caravan road",
            },
            "mosul": {
                "distance": 4,
                "danger": 3,
                "route_name": "Upper river road",
            },
        },
    },

    "baghdad": {
        "name": "Baghdad",
        "description": "The great city of learning, luxury goods, and ambitious merchants.",
        "connections": {
            "damascus": {
                "distance": 5,
                "danger": 3,
                "route_name": "Western desert road",
            },
            "mosul": {
                "distance": 3,
                "danger": 2,
                "route_name": "Tigris road",
            },
        },
    },

    "mosul": {
        "name": "Mosul",
        "description": "A northern city of bridges, caravanserais, and frontier rumors.",
        "connections": {
            "aleppo": {
                "distance": 4,
                "danger": 3,
                "route_name": "Syrian road",
            },
            "baghdad": {
                "distance": 3,
                "danger": 2,
                "route_name": "Southern river road",
            },
        },
    },
}