from items.item import Item


class Weapon(Item):
    def __init__(self, name, rarity, dmg, luck, effect=None):
        super().__init__(name, rarity, effect)
        self.dmg = dmg
        self.luck = luck
        self.description += "   Damage: " + str(self.dmg)
        if self.effect != None:
            self.description += "\n   Effect: " + self.effect.description
