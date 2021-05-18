from locations.forest import Forest
from entities.NPCs import Merchant
from items.globals import stick, elixirRecov

from managers.battle import Battle
import random
from time import sleep


class Game:
    def __init__(self, player):
        self.player = player

    def engageBattle(self, battle):
        battle.battleLoop()

    def enterArea(self):
        newForest = Forest(self.player)
        newForest.enter()
        self.player.enteredArea = True
        self.area = newForest

    def idle(self):
        self.eventOccured = False
        choice = 0
        while choice != "1" or choice != "4":
            # self.eventOccured = False
            if self.player.enteredArea == False:
                self.enterArea()
            sleep(0.5)

            self.eventOccured = self.area.events(self.eventOccured)
            self.randMerchEvent()

            sleep(0.5)
            print("\nWhat would you like to do?")
            choice = input(
                "[1]Fight an enemy \n[2]Open Inventory  \n[3]Check Stats \n[4]Boss Fight\nEnter Choice: "
            )

            if choice == "3":
                self.player.displayStats()

            elif choice == "2":
                self.player.checkInventory()
                self.player.invOptions()

            elif choice == "1":
                sleep(0.5)
                areaBattle = Battle(self.player, self.area.chooseMonster())
                self.engageBattle(areaBattle)

            elif choice == "4":
                sleep(0.5)
                boss = self.area.chooseBoss()
                if boss:
                    bossBattle = Battle(self.player, boss)
                    sleep(0.5)
                    boss.oneLiner()
                    sleep(2)
                    self.engageBattle(bossBattle)
                    if boss.hp <= 0:  # If player dies
                        self.area.bosses.append(boss)
                else:
                    sleep(0.5)
                    print("\nAll bosses in %s have been defeated!" % self.area.name)
                    sleep(1.5)
            else:
                print("Please enter a proper choice.")

    def merchantEncounter(self):
        names = ["Robert", "Bob", "Dervin", "Lucario"]
        randomName = names[random.randint(0, len(names) - 1)]
        merchant = Merchant(randomName, [stick, elixirRecov])

        print("\n%s encountered %s the Merchant!" % (self.player.name, merchant.name))
        choice = 0
        while choice != "2":
            print("\nWhat will you do?")
            choice = input("[1]Talk \n[2]Leave \nEnter Choice: ")
            if choice == "1":
                merchant.showStock()
                merchant.options(self.player)

    def randMerchEvent(self):
        if self.eventOccured == False:
            num = random.randint(1, 10)
            if num <= 3:
                self.eventOccured = True
                self.merchantEncounter()
