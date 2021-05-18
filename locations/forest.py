from locations.area import Area
import random
from time import sleep

from entities.enemies.enemies import Bat, Serpent, AntArmy, DustElemental
from entities.enemies.bosses.bosses import Treant, QueenBee
from entities.NPCs import Druid


class Forest(Area):
    def __init__(self, player):
        self.name = "The Forest"
        self.player = player
        self.bosses = [Treant(), QueenBee()]

    def chooseMonster(self):
        self.monsters = [Bat(), Serpent(), AntArmy(), DustElemental()]
        monster = random.choice(self.monsters)
        return monster

    def chooseBoss(self):
        if len(self.bosses) > 0:
            boss = random.choice(self.bosses)
            self.bosses.remove(boss)
        else:
            boss = False
        return boss

    def druidEncounter(self):
        druid = Druid()
        print("\n%s encountered the %s!" % (self.player.name, druid.name))
        sleep(0.5)
        choice = 0
        druid.optionsIntro(self.player)
        sleep(3)

    def druidEvent(self, eventOcc):
        if eventOcc == False:
            num = random.randint(1, 7)
            if num == 1:
                self.druidEncounter()
                # print ("Returns a special", True)
                return True
        # print ("Returns a", eventOccured)
        return False

    def events(self, eventOcc):
        eventOccured = eventOcc
        if eventOccured == False:
            eventOccured = self.druidEvent(eventOccured)
        # print ("Returns", eventOccured)
        return eventOccured
