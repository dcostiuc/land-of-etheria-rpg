from entities.enemies.enemy import Enemy
from entities.globals import player1
from items.globals import (
    stick,
    claw,
    batBat,
    batWing,
    vampArmor,
    fang,
    eyeSerpent,
    vipBlade,
    snakeHide,
    vileVenom,
    bottleAnts,
    deadAnt,
    giantPincers,
    elemSoul,
    organs,
    skull,
    slayerBeast,
    spikedPelt,
)

import random


# Enemy Classess
class Bat(Enemy):
    def __init__(self):
        prefix = {1: "Angry", 2: "Scary", 3: "Mad", 4: "Sneaky", 5: "Scaly"}
        self.name = prefix[random.randint(1, 5)] + " Bat"
        self.hp = random.randint(1, 5) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 5 + random.randint(0, player1.lvl)
        self.xp = random.randint(1, xpMax)
        self.dmg = 5
        self.lowest = 1

        self.items = [stick, claw, batBat, batWing, vampArmor]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 5
        self.lvl = random.randint(1, player1.lvl)


class Serpent(Enemy):
    def __init__(self):
        prefix = {
            1: "Slippery",
            2: "Venomous",
            3: "Cold-Blooded",
            4: "Sharp-Fanged",
            5: "Sneaky",
        }
        self.name = prefix[random.randint(1, 5)] + " Serpent"
        self.hp = random.randint(1, 3) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 5 + random.randint(0, player1.lvl)
        self.xp = random.randint(1, xpMax)
        self.dmg = 7
        self.lowest = 1

        self.items = [fang, eyeSerpent, vipBlade, snakeHide, vileVenom]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 5
        self.lvl = random.randint(1, player1.lvl)


class AntArmy(Enemy):
    def __init__(self):
        prefix = {
            1: "Ferocious",
            2: "Violent",
            3: "Merciless",
            4: "Ruthless",
            5: "Voracious",
        }
        self.name = prefix[random.randint(1, 5)] + " Ant Army"
        self.hp = 1 + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 1 + random.randint(0, player1.lvl)
        self.xp = random.randint(1, xpMax)
        self.dmg = 10
        self.lowest = 1

        self.items = [bottleAnts, deadAnt, giantPincers]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 5
        self.lvl = random.randint(1, player1.lvl)


class DustElemental(Enemy):
    def __init__(self):
        prefix = {1: "Windy", 2: "Gusty", 3: "Gaseous", 4: "Stormy", 5: "Febreezy"}
        self.name = prefix[random.randint(1, 5)] + " Dust Elemental"
        self.hp = random.randint(1, 7) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 5 + random.randint(0, player1.lvl)
        self.xp = random.randint(1, xpMax)
        self.dmg = 2
        self.lowest = 1

        self.items = [elemSoul]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 5
        self.lvl = random.randint(1, player1.lvl)


class CreatureDepths(Enemy):
    def __init__(self):
        prefix = {
            1: "Malicious",
            2: "Bloodcurdling",
            3: "Unknown",
            4: "Savage",
            5: "Ancient",
        }
        self.name = prefix[random.randint(1, 5)] + " Creature of the Depths"
        self.hp = random.randint(1, 5) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 8 + random.randint(0, player1.lvl)
        self.xp = random.randint(1, xpMax)
        self.dmg = 10
        self.lowest = 1

        self.items = [organs, skull, slayerBeast, spikedPelt]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 8
        self.lvl = random.randint(1, player1.lvl)
