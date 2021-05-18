from time import sleep
import random

from items.weapon import Weapon
from items.armor import Armor
from items.potion import Potion
from items.globals import (
    protector,
    vileVenom,
    jarHoney,
    potFlames,
    elixirRecov,
    potFury,
    fists,
)

# include Battle?
class Player:
    def __init__(self, hp, startingItem, startingArmor, name="Player"):
        self.hp = hp
        self.maxHp = hp
        self.name = name
        self.xp = 0
        self.inv = [protector, vileVenom, jarHoney, potFlames, elixirRecov, potFury]
        self.equippedWeapon = startingItem
        self.equippedArmor = protector  # startingArmor
        self.dmg = self.equippedWeapon.dmg
        self.defence = self.equippedArmor.defence
        self.luck = 1
        self.lvl = 1
        self.cap = 5
        self.cash = 0
        self.enteredArea = False

    def displayStats(self):
        print("\nSTATS")
        print("------")
        print(
            "\n Name: %s      Level: %d       XP: %d" % (self.name, self.lvl, self.xp)
        )
        print(
            "\n HP: %d/%d       Max Damage: %d       Armor: %d       Luck: %d"
            % (self.hp, self.maxHp, self.dmg, self.defence, self.luck)
        )

    def attack(self, enemy):
        self.critHit = False
        self.atk = random.randint(0, self.dmg)

        if random.randint(1, 10) <= self.luck:
            self.crit()
        enemy.hp -= self.atk

        if self.critHit:
            print(
                "\n%s attacked %s. It was a critical hit! %s dealt %d damage."
                % (self.name, enemy.name, self.name, self.atk)
            )
            sleep(2)
        else:
            print(
                "\n%s attacked %s, dealing %d damage!"
                % (self.name, enemy.name, self.atk)
            )
            sleep(2)

    def crit(self):
        self.atk *= 2
        self.critHit = True

    def gainXp(self, gain):
        self.xp += gain
        print("\n%s gained %d experience points!" % (self.name, gain))
        if self.xp == self.cap:
            sleep(3)
            self.lvlUp()
        while self.xp > self.cap:
            sleep(2)
            self.lvlUp()

    def lvlUp(self):
        self.lvl += 1
        self.xp = abs(self.cap - self.xp)
        self.cap += self.lvl * 2
        self.maxHp += 2
        self.hp = self.maxHp
        print(
            "\nOoh! %s leveled up!\n %s is now level %d."
            % (self.name, self.name, self.lvl)
        )

    def battleChoices(self, enemy, battle):
        choice = 0
        while choice != "4":
            choice = input(
                "\n[1]Attack \n[2]Special Abilities \n[3]Inventory \n[4]Run \nEnter Choice: "
            )
            if choice == "1":
                self.attack(enemy)
                return False
            elif choice == "2":
                self.displayAbilities()
                choice = self.abilityOptions(enemy, battle)
                if choice != "3":
                    return False
            elif choice == "3":
                self.checkInventory()
            elif choice == "4":
                return True
            else:
                print("Please enter a proper command.")

    def displayAbilities(self):
        sleep(0.5)
        potions = []
        print("\nABILITIES")
        print("----------")
        print("Item Effects:")
        if self.equippedWeapon.effect:
            print(
                "*%s (from %s)" % (self.equippedWeapon.effect.name, self.equippedWeapon)
            )
            print("   %s" % self.equippedWeapon.effect.description)
        if self.equippedArmor.effect:
            print(
                "\n*%s (from %s)" % (self.equippedArmor.effect.name, self.equippedArmor)
            )
            print("   %s" % self.equippedArmor.effect.description)
        print("\nPotions:")
        for item in self.inv:
            if type(item) is Potion:
                print("\n*%s (from %s)" % (item.effect.name, item))
                print("   %s" % item.effect.description)

    def useItem(self, item, enemy=None, battle=None):
        if item.effect.turns > 1 and item.effect.affects == "player":
            battle.playerTurnEffects.append(item.effect)
            item.effect.turnsLeft -= 1
        elif item.effect.turns > 1 and item.effect.affects == "enemy":
            battle.enemyTurnEffects.append(item.effect)
            item.effect.turnsLeft -= 1
        item.effect.mainEffect(item.effect.effectActivator, enemy)

    def abilityOptions(self, enemy, battle):
        self.enemy = enemy
        choice = 0
        choice = input("\n[1]Activate Item \n[2]Use Potion \n[3]Back \nEnter Choice: ")
        if choice == "1":
            sleep(0.5)
            itemName = input("\nType the name of the ITEM you want to activate: ")

            if self.equippedWeapon.name.lower() == itemName.lower():
                item = self.equippedWeapon
                self.useItem(item, self.enemy, battle)
                if item.effect.oneUse:
                    item.effect = None
            elif self.equippedArmor.name.lower() == itemName.lower():
                item = self.equippedArmor
                self.useItem(item, self.enemy, battle)
                if item.effect.oneUse:
                    item.effect = None
            else:
                print("The item you have entered did not work.")
            sleep(0.5)

        elif choice == "2":
            sleep(0.5)
            potionName = input("\nType the name of the POTION you want to use: ")

            potion = self.itemSearch(potionName)
            sleep(0.5)
            self.useItem(potion, self.enemy, battle)
            self.removeItem(potion)
            sleep(1)

        elif choice == "3":
            sleep(0.5)

        else:
            print("Please enter a proper command.")
            print("")
        return choice

    def checkInventory(self):
        sleep(0.5)
        print("\nINVENTORY")
        print("---------")
        for item in self.inv:
            print("\n*%s" % item)
            item.info()
        print("\nGold: %d" % self.cash)
        self.checkEquipped()

    def checkEquipped(self):
        print("\nEquipped Weapon: %s" % self.equippedWeapon)
        print("\nEquipped Armor: %s" % self.equippedArmor)
        sleep(2)

    def invOptions(self):
        choice = 0
        while choice != "3":
            choice = input(
                "[1]Equip Weapon \n[2]Equip Armor \n[3]Leave \nEnter Choice: "
            )
            if choice == "1":
                sleep(0.5)
                try:
                    self.showWeapons()
                    wepName = input("\nType the name of the weapon you want to equip: ")

                    weapon = self.itemSearch(wepName)

                    self.equipWeapon(weapon)
                    sleep(0.5)
                except (ValueError, AttributeError):
                    # print("Weapon was not found.")
                    pass

            elif choice == "2":
                sleep(0.5)
                try:
                    self.showArmor()
                    armName = input("\nType the name of the armor you want to equip: ")

                    armor = self.itemSearch(armName.lower())

                    self.equipArmor(armor)
                    sleep(0.5)

                except (ValueError, AttributeError):
                    # print("Armor was not found.")
                    pass

            elif choice == "3":
                pass
            else:
                print("Please enter a proper command.")
            print("")

    def showWeapons(self):
        print("\nWEAPONS:")
        for item in self.inv:
            if type(item) is Weapon:
                print("*%s" % item)

    def showArmor(self):
        print("\nARMOR:")
        for item in self.inv:
            if type(item) is Armor:
                print("*%s" % item)

    def itemSearch(self, itemName):
        # Conducts a linear search for the item
        itemNeeded = 0
        for item in self.inv:
            if item.name.lower() == itemName.lower():
                itemNeeded = item
        return itemNeeded

    def addItem(self, item):
        self.inv.append(item)

    def equipWeapon(self, weapon):
        if self.equippedWeapon != fists:
            self.inv.append(self.equippedWeapon)
        self.luck -= self.equippedWeapon.luck
        self.equippedWeapon = weapon
        self.inv.remove(self.equippedWeapon)
        self.dmg = self.equippedWeapon.dmg
        self.luck += self.equippedWeapon.luck
        print("%s was equipped." % self.equippedWeapon)

    def equipArmor(self, armor):
        self.inv.append(self.equippedArmor)
        self.luck -= self.equippedArmor.luck
        self.equippedArmor = armor
        self.inv.remove(armor)
        self.defence = self.equippedArmor.defence
        self.luck += self.equippedArmor.luck
        print("%s was equipped." % self.equippedArmor)

    def loot(self, enemy):
        for item in enemy.inv:
            self.addItem(item)
        self.cash += enemy.amount

    def sellItem(self, item, npc):
        self.inv.remove(item)
        npc.inv.append(item)
        self.cash += item.price
        print("You have sold %s to %s for %d gold." % (item, npc.name, item.price))
        sleep(2)

    def buyItem(self, item, npc):
        self.cash -= item.price
        npc.inv.remove(item)
        self.inv.append(item)
        print("You bought %s from %s for %d gold." % (item, npc.name, item.price))
        sleep(2)

    def removeItem(self, item):
        self.inv.remove(item)
