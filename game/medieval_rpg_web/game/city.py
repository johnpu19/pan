class City:
    def __init__(self, name, market):
        self.name = name
        self.market = market  # Dictionary like {"Spices": {"buy": 10, "sell": 8}}

    def get_buy_price(self, item):
        return self.market.get(item, {}).get('buy')

    def get_sell_price(self, item):
        return self.market.get(item, {}).get('sell')

    def has_item(self, item):
        return item in self.market

    def to_dict(self):
        return {
            "name": self.name,
            "market": self.market
        }

    @staticmethod
    def from_dict(data):
        return City(data['name'], data['market'])