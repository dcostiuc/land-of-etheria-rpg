import random

import entities.globals


class Effect:
    def __init__(self, name, description, turns, amount, affects, rand=False):
        self.name = name
        self.description = description
        self.amount = amount
        self.turns = turns
        self.turnsLeft = turns
        self.affects = affects
        self.rand = rand
        self.effectActivator = None
        self.oneUse = True

    def setRandLimits(self, lower, upper):
        if self.rand:
            self.lower = lower
            self.upper = upper

    def mainEffect(self, eff, enemy=None):
        if eff == "heal":
            self.heal()
        elif eff == "dmg":
            self.dmg(enemy)
        elif eff == "dmginc":
            self.dmgIncrease(enemy)

    def heal(self):
        if self.rand:
            self.amount = random.randint(self.lower, self.upper)
            entities.globals.player1.hp += self.amount
        else:
            entities.globals.player1.hp += self.amount
        if entities.globals.player1.hp > entities.globals.player1.maxHp:
            entities.globals.player1.hp = entities.globals.player1.maxHp
        print(
            "\n%s's %s has healed them for %d damage. (%d turns remaining)"
            % (entities.globals.player1.name, self.name, self.amount, self.turnsLeft)
        )

    def dmg(self, enemy):
        if self.rand:
            self.amount = random.randint(self.lower, self.upper)
            enemy.hp -= self.amount
        else:
            enemy.hp -= self.amount
        print(
            "\n%s's %s delt %d damage to %s. (%d turns remaining)"
            % (
                entities.globals.player1.name,
                self.name,
                self.amount,
                enemy.name,
                self.turnsLeft,
            )
        )

    def dmgIncrease(self, enemy):
        originalDmg = entities.globals.player1.dmg
        entities.globals.player1.dmg = int(entities.globals.player1.dmg * self.amount)
        amt = entities.globals.player1.dmg
        print(
            "\n%s's Max Damage has been amplified by %d through %s. (%d turns remaining)"
            % (entities.globals.player1.name, self.amount, self.name, self.turnsLeft)
        )
        if self.turnsLeft == 0 or (enemy.hp - amt <= 0):
            entities.globals.player1.dmg = originalDmg
            print("Damage has been returned to normal (for the sake of the player).")
