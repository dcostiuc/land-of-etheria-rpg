# In-game objects
class Item:
    def __init__(self, name, rarity, effect=None):
        rarities = {
            -1: "Special",
            0: "Garbage",
            1: "Abyssmal",
            2: "Basic",
            3: "Common",
            4: "Uncommon",
            5: "Rare",
            6: "Very Rare",
            7: "Limited",
            8: "Godlike",
            9: "Unique",
        }
        self.name = name
        self.rarityName = rarities[rarity]
        self.rarity = rarity
        self.price = 5 * rarity
        self.description = self.setDescription()
        self.effect = effect
        # if self.effect != None:
        # self.description += "   Effect: " + self.effect.description
        self.oneUse = False

    def __str__(self):
        return self.name

    def setDescription(self):
        description = (
            "     Rarity: "
            + str(self.rarityName)
            + "   Price: "
            + str(self.price)
            + " G"
        )
        return description

    def info(self):
        print(self.description)


class Consumable(Item):
    def __init__(self, name, rarity, effect):
        super().__init__(name, rarity)
        self.consumable = True
        self.effect = effect
        if self.effect != None:
            self.description += "\n   Effect: " + self.effect.description
