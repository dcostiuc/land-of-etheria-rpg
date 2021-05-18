from entities.enemies.bosses.boss import Boss
from entities.enemies.enemy import Enemy
from entities.globals import player1
from items.globals import (
    stick,
    timber,
    lumber,
    clubThorns,
    protector,
    nectar,
    honeycomb,
    sting,
    jarHoney,
)

import random
from time import sleep


# Boss Classes
class Treant(Boss):
    def __init__(self):
        self.name = "The Treant"
        self.hp = random.randint(10, 15) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 10 + random.randint(0, player1.lvl)
        self.xp = random.randint(6, xpMax)
        self.dmg = 11
        self.lowest = 7

        self.items = [stick, timber, lumber, clubThorns, protector]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 10
        self.lvl = random.randint(1, 15 + player1.lvl)

        self.line = '\n"By the spirits of the forest, I will condemn thee!"'

    def ability(self):
        amount = 5
        self.hp += 5
        if self.hp > self.maxHp:
            self.hp = self.maxHp
        sleep(0.5)
        print("\n%s used Regrowth! 5 HP was restored." % (self.name))
        sleep(1.5)


class QueenBee(Boss):
    def __init__(self):
        self.name = "The Queen Bee"
        self.hp = random.randint(9, 17) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 15 + random.randint(0, player1.lvl)
        self.xp = random.randint(9, xpMax)
        self.dmg = 14
        self.lowest = 7

        self.items = [nectar, honeycomb, sting, jarHoney]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 13
        self.lvl = random.randint(1, 15 + player1.lvl)

        self.line = '\n"What does a human want with my buzzful fuzz?"'

    def attack(self, enemy):
        choice = random.randint(1, 3)
        if choice == 1:
            atk = self.dmg - enemy.defence
            enemy.hp -= atk
            sleep(0.5)
            print(
                "\n%s was attacked with a Critical Stinger, striken with %d damage!"
                % (enemy.name, atk)
            )
            sleep(2)
        else:
            Enemy.attack(self, enemy)
