from items.item import Consumable


class Potion(Consumable):
    def __init__(self, name, rarity, effect):
        super().__init__(name, rarity, effect)
