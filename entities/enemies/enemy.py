import random
from time import sleep


class Enemy:
    def __init__(self, hp, dmg, name, xpMax, items):
        self.hp = hp
        self.maxHp = hp
        self.dmg = dmg
        self.name = name
        self.xp = random.randint(1, xpMax)
        self.inv = items
        self.lowest = 1

    def displayStats(self):
        print("\nSTATS")
        print("------")
        print("\n Name: %s      Level: %d" % (self.name, self.lvl))
        print("\n HP: %d/%d       Max Damage: %d " % (self.hp, self.maxHp, self.dmg))

    def attack(self, enemy):
        atk = random.randint(self.lowest, self.dmg) - enemy.defence
        if atk < 0:
            atk = 0
        enemy.hp -= atk
        print("\n%s attacked %s, dealing %d damage!" % (self.name, enemy.name, atk))
        sleep(2)

    def dropItems(self):
        print("\n%s dropped:" % self.name)
        for item in self.inv:
            print("*%s" % item)
        self.dropGold()

    def dropGold(self):
        self.amount = random.randint(0, self.upperGold)
        print("*%s Gold" % str(self.amount))

    def possibleLoot(self):
        loot = []

        # Creates a new list of loot, where the probability to drop something is now closer related to its rarity
        for each in self.items:
            for each2 in range((10 - each.rarity) ** 2):
                loot.append(each)
        random.shuffle(loot)
        return loot

    def createDropped(self):
        dropped = []
        numItems = random.randint(1, 2)
        for eachItem in range(numItems):
            randItem = random.randint(0, len(self.loot) - 1)
            dropped.append(self.loot[randItem])
        return dropped


# class CreateMonster:
#     def __init__(self):
#         pass

#     def createBat(self, items):
#         newBat = Bat(items)
#         return newBat
