from entities.enemies.enemy import Enemy

import random
from time import sleep


class Boss(Enemy):
    def __init__(self, hp, dmg, name, xpMax, items):
        super().__init__(hp, dmg, name, xpMax, items)
        self.line = ""

    def oneLiner(self):
        print(self.line)
        sleep(1)

    def ability(self):
        pass

    def attack(self, enemy):
        choice = random.randint(1, 3)
        if choice == 1:
            self.ability()  # Might be problems with self
        else:
            super().attack(enemy)
