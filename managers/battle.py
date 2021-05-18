from time import sleep

from entities.enemies.bosses.boss import Boss
from entities.player import Player


class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.playerTurnEffects = []
        self.enemyTurnEffects = []

    def start(self):
        if issubclass(type(self.enemy), Boss):
            print("\nOh wow! %s has met %s!" % (self.player.name, self.enemy.name))
        else:
            print("\nOh! %s encountered a(n) %s!" % (self.player.name, self.enemy.name))
        sleep(2)

    def turn(self, entity):
        print("\n\nIt's %s's turn!" % (entity.name))
        sleep(2)
        # entity.displayStats()
        if type(entity) is Player:  # or do entity is self.player
            sleep(0.5)
            for effect in self.playerTurnEffects:
                effect.turnsLeft -= 1
                effect.mainEffect(effect.effectActivator, self.enemy)
                sleep(1)
                if effect.turnsLeft == 0:
                    self.playerTurnEffects.remove(effect)
            sleep(0.5)
            entity.displayStats()
            run = entity.battleChoices(self.enemy, self)
            # print(run)
            return run
        else:
            for effect in self.enemyTurnEffects:
                effect.turnsLeft -= 1
                effect.mainEffect(effect.effectActivator, self.enemy)
                sleep(1)
                if effect.turnsLeft == 0:
                    self.enemyTurnEffects.remove(effect)
            sleep(0.5)
            entity.displayStats()
            entity.attack(self.player)

        if self.player.hp > self.player.maxHp:
            self.player.hp = self.player.maxHp

    def victory(self):
        print(
            "\nCongratulations %s, you defeated %s."
            % (self.player.name, self.enemy.name)
        )
        sleep(3)
        self.player.gainXp(self.enemy.xp)
        sleep(3)
        self.enemy.dropItems()
        choice = input("[1]Loot \n[2]Leave \nEnter Choice: ")
        print("\n")
        if choice == "1":
            self.player.loot(self.enemy)
        del self.enemy

    def defeat(self):
        sleep(1)
        print("You were defeated by %s!" % (self.enemy.name))
        sleep(2)
        print(
            "\n\nYou were reborn, but sadly lost all of your gold and inventory \nthrough the soul transference process."
        )
        self.player.hp = self.player.maxHp
        self.player.cash = 0
        self.player.inv = []
        sleep(4)

    def battleLoop(self):
        run = False
        self.start()
        while (self.player.hp > 0 and self.enemy.hp > 0) and run == False:
            run = self.turn(self.player)
            sleep(2)
            if run == True:
                print("%s ran away!" % self.player.name)
                sleep(0.5)
            elif self.enemy.hp > 0:
                self.turn(self.enemy)
                sleep(2)
        if self.player.hp <= 0:
            self.defeat()
        elif self.enemy.hp <= 0:
            self.victory()
