from items.item import Item


class Armor(Item):
    def __init__(self, name, rarity, defence, luck, effect=None):
        super().__init__(name, rarity, effect)
        self.effect = effect
        self.defence = defence
        self.luck = luck
        self.description += "   Defence: " + str(self.defence)
        if self.effect != None:
            self.description += "\n   Effect: " + self.effect.description
