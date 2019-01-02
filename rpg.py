import random
from time import *

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.playerTurnEffects = []
        self.enemyTurnEffects = []

    def start(self):
        if issubclass(type(self.enemy), Boss):
            print("\nOh wow! %s has met %s!" %(self.player.name, self.enemy.name))
        else:
            print("\nOh! %s encountered a(n) %s!" %(self.player.name, self.enemy.name))
        sleep(2)

    def turn(self, entity):
        print("\n\nIt's %s's turn!" %(entity.name))
        sleep(2)
        #entity.displayStats()
        if type(entity) is Player: #or do entity is self.player
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
            #print(run)
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
        print("\nCongratulations %s, you defeated %s." %(self.player.name, self.enemy.name))
        sleep(3)
        self.player.gainXp(self.enemy.xp)
        sleep(3)
        self.enemy.dropItems()
        choice = input("[1]Loot \n[2]Leave \nEnter Choice: ")
        print("\n")
        if choice == '1':
            self.player.loot(self.enemy)
        del self.enemy

    def defeat(self):
        sleep(1)
        print("You were defeated by %s!" %(self.enemy.name))
        sleep(2)
        print("\n\nYou were reborn, but sadly lost all of your gold and inventory \nthrough the soul transference process.")
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
                print("%s ran away!" %self.player.name)
                sleep(0.5)
            elif self.enemy.hp >  0:
                self.turn(self.enemy)
                sleep(2)
        if self.player.hp <= 0:
            self.defeat()
        elif self.enemy.hp <= 0:
            self.victory()




class Player(Battle):
    def __init__(self, hp, startingItem, startingArmor, name = "Player"):
        self.hp = hp
        self.maxHp = hp
        self.name = name
        self.xp = 0
        self.inv = [protector, vileVenom, jarHoney, potFlames, elixirRecov, potFury]
        self.equippedWeapon = startingItem
        self.equippedArmor = protector#startingArmor
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
        print("\n Name: %s      Level: %d       XP: %d" %(self.name, self.lvl, self.xp))
        print("\n HP: %d/%d       Max Damage: %d       Armor: %d       Luck: %d" %(self.hp, self.maxHp, self.dmg, self.defence, self.luck))

    def attack(self, enemy):
        self.critHit = False
        self.atk = random.randint(0, self.dmg)

        if random.randint(1,10) <= self.luck:
            self.crit()
        enemy.hp -= self.atk

        if self.critHit:
            print ("\n%s attacked %s. It was a critical hit! %s dealt %d damage." %(self.name, enemy.name, self.name, self.atk))
            sleep(2)
        else:
            print("\n%s attacked %s, dealing %d damage!" %(self.name, enemy.name, self.atk))
            sleep(2)


    def crit(self):
        self.atk *= 2
        self.critHit = True

    def gainXp(self, gain):
        self.xp += gain
        print("\n%s gained %d experience points!" %(self.name, gain))
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
        print("\nOoh! %s leveled up!\n %s is now level %d." %(self.name, self.name, self.lvl))

    def battleChoices(self, enemy, battle):
        choice = 0
        while choice != '4':
            choice = input("\n[1]Attack \n[2]Special Abilities \n[3]Inventory \n[4]Run \nEnter Choice: ")
            if choice == '1':
                self.attack(enemy)
                return False
            elif choice == '2':
                self.displayAbilities()
                choice = self.abilityOptions(enemy, battle)
                if choice != '3':
                    return False
            elif choice == '3':
                self.checkInventory()
            elif choice == '4':
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
            print ("*%s (from %s)" %(self.equippedWeapon.effect.name, self.equippedWeapon))
            print ("   %s" %self.equippedWeapon.effect.description)
        if self.equippedArmor.effect:
            print ("\n*%s (from %s)" %(self.equippedArmor.effect.name, self.equippedArmor))
            print ("   %s" %self.equippedArmor.effect.description)
        print("\nPotions:")
        for item in self.inv:
            if type(item) is Potion:
                print ("\n*%s (from %s)" %(item.effect.name, item))
                print ("   %s" %item.effect.description)


    def useItem(self, item, enemy = None, battle = None):
        if item.effect.turns > 1 and item.effect.affects == 'player':
            battle.playerTurnEffects.append(item.effect)
            item.effect.turnsLeft -= 1
        elif item.effect.turns > 1 and item.effect.affects == 'enemy':
            battle.enemyTurnEffects.append(item.effect)
            item.effect.turnsLeft -= 1
        item.effect.mainEffect(item.effect.effectActivator, enemy)


    def abilityOptions(self, enemy, battle):
        self.enemy = enemy
        choice = 0
        choice = input("\n[1]Activate Item \n[2]Use Potion \n[3]Back \nEnter Choice: ")
        if choice == '1':
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

        elif choice == '2':
            sleep(0.5)
            potionName = input("\nType the name of the POTION you want to use: ")

            potion = self.itemSearch(potionName)
            sleep(0.5)
            self.useItem(potion, self.enemy, battle)
            self.removeItem(potion)
            sleep(1)

        elif choice == '3':
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
            print ("\n*%s" %item)
            item.info()
        print("\nGold: %d" %self.cash)
        self.checkEquipped()

    def checkEquipped(self):
        print("\nEquipped Weapon: %s" %self.equippedWeapon)
        print("\nEquipped Armor: %s" %self.equippedArmor)
        sleep(2)

    def invOptions(self):
        choice = 0
        while choice != '3':
            choice = input("[1]Equip Weapon \n[2]Equip Armor \n[3]Leave \nEnter Choice: ")
            if choice == '1':
                sleep(0.5)
                try:
                    self.showWeapons()
                    wepName = input("\nType the name of the weapon you want to equip: ")

                    weapon = self.itemSearch(wepName)

                    self.equipWeapon(weapon)
                    sleep(0.5)
                except (ValueError, AttributeError):
                    #print("Weapon was not found.")
                    pass


            elif choice == '2':
                sleep(0.5)
                try:
                    self.showArmor()
                    armName = input("\nType the name of the armor you want to equip: ")

                    armor = self.itemSearch(armName.lower())

                    self.equipArmor(armor)
                    sleep(0.5)

                except (ValueError, AttributeError):
                    #print("Armor was not found.")
                    pass


            elif choice == '3':
                pass
            else:
                print("Please enter a proper command.")
            print("")

    def showWeapons(self):
        print("\nWEAPONS:")
        for item in self.inv:
            if type(item) is Weapon:
                print("*%s" %item)

    def showArmor(self):
        print("\nARMOR:")
        for item in self.inv:
            if type(item) is Armor:
                print("*%s" %item)

    def itemSearch(self, itemName):
    #Conducts a linear search for the item
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
        print("%s was equipped." %self.equippedWeapon)

    def equipArmor(self, armor):
        self.inv.append(self.equippedArmor)
        self.luck -= self.equippedArmor.luck
        self.equippedArmor = armor
        self.inv.remove(armor)
        self.defence = self.equippedArmor.defence
        self.luck += self.equippedArmor.luck
        print("%s was equipped." %self.equippedArmor)

    def loot(self, enemy):
        for item in enemy.inv:
                self.addItem(item)
        self.cash += enemy.amount

    def sellItem(self, item, npc):
        self.inv.remove(item)
        npc.inv.append(item)
        self.cash += item.price
        print("You have sold %s to %s for %d gold." %(item, npc.name, item.price))
        sleep(2)

    def buyItem(self, item, npc):
        self.cash -= item.price
        npc.inv.remove(item)
        self.inv.append(item)
        print("You bought %s from %s for %d gold." %(item, npc.name, item.price))
        sleep(2)

    def removeItem(self, item):
        self.inv.remove(item)

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
        print("\n Name: %s      Level: %d" %(self.name, self.lvl))
        print("\n HP: %d/%d       Max Damage: %d " %(self.hp, self.maxHp, self.dmg))

    def attack(self, enemy):
        atk = random.randint(self.lowest, self.dmg) - enemy.defence
        if atk < 0:
            atk = 0
        enemy.hp -= atk
        print("\n%s attacked %s, dealing %d damage!" %(self.name, enemy.name, atk))
        sleep(2)

    def dropItems(self):
        print("\n%s dropped:" %self.name)
        for item in self.inv:
                print("*%s" %item)
        self.dropGold()

    def dropGold(self):
        self.amount = random.randint(0,self.upperGold)
        print("*%s Gold" %str(self.amount))


    def possibleLoot(self):
        loot = []

        #Creates a new list of loot, where the probability to drop something is now closer related to its rarity
        for each in self.items:
            for each2 in range ((10 - each.rarity)**2):
                loot.append(each)
        random.shuffle(loot)
        return loot

    def createDropped(self):
        dropped = []
        numItems = random.randint(1,2)
        for eachItem in range (numItems):
            randItem = random.randint(0, len(self.loot) - 1)
            dropped.append(self.loot[randItem])
        return dropped

class Boss (Enemy):
    def __init__(self, hp, dmg, name, xpMax, items):
        super().__init__(hp, dmg, name, xpMax, items)
        self.line = ""

    def oneLiner(self):
        print(self.line)
        sleep(1)

    def ability(self):
        pass

    def attack(self, enemy):
        choice = random.randint(1,3)
        if choice == 1:
            self.ability() #Might be problems with self
        else:
            super().attack(enemy)

#Boss Classes
class Treant (Boss):
    def __init__(self):
        self.name = "The Treant"
        self.hp = random.randint(10,15) + random.randint(0, player1.lvl)
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
        print("\n%s used Regrowth! 5 HP was restored." %(self.name))
        sleep(1.5)



class QueenBee (Boss):
    def __init__(self):
        self.name = "The Queen Bee"
        self.hp = random.randint(9,17) + random.randint(0, player1.lvl)
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
        choice = random.randint(1,3)
        if choice == 1:
            atk = self.dmg - enemy.defence
            enemy.hp -= atk
            sleep(0.5)
            print("\n%s was attacked with a Critical Stinger, striken with %d damage!" %(enemy.name, atk))
            sleep(2)
        else:
            Enemy.attack(self, enemy)


#Enemy Classes

class Bat (Enemy):
    def __init__(self):
        prefix = {1: "Angry", 2: "Scary", 3: "Mad", 4: "Sneaky", 5 : "Scaly"}
        self.name = prefix [random.randint(1,5)] + " Bat"
        self.hp = random.randint(1,5) + random.randint(0, player1.lvl)
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
        prefix = {1: "Slippery", 2: "Venomous", 3: "Cold-Blooded", 4: "Sharp-Fanged", 5 : "Sneaky"}
        self.name = prefix [random.randint(1,5)] + " Serpent"
        self.hp = random.randint(1,3) + random.randint(0, player1.lvl)
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
        prefix = {1: "Ferocious", 2: "Violent", 3: "Merciless", 4: "Ruthless", 5 : "Voracious"}
        self.name = prefix [random.randint(1,5)] + " Ant Army"
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
        prefix = {1: "Windy", 2: "Gusty", 3: "Gaseous", 4: "Stormy", 5 : "Febreezy"}
        self.name = prefix [random.randint(1,5)] + " Dust Elemental"
        self.hp = random.randint(1,7) + random.randint(0, player1.lvl)
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
        prefix = {1: "Malicious", 2: "Bloodcurdling", 3: "Unknown", 4: "Savage", 5 : "Ancient"}
        self.name = prefix [random.randint(1,5)] + " Creature of the Depths"
        self.hp = random.randint(1,5) + random.randint(0, player1.lvl)
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



class CrimsonCommunist(Enemy):
    def __init__(self):
        self.name = "Crimson Communist"
        self.hp = random.randint(1,20) + random.randint(0, player1.lvl)
        self.maxHp = self.hp
        xpMax = 10 + random.randint(0, player1.lvl)
        self.xp = random.randint(1, xpMax)
        self.dmg = 10
        self.lowest = 5

        self.items = [crimFlag, goldHammer, goldSickle, redNation, potFury]
        self.loot = self.possibleLoot()
        self.inv = self.createDropped()

        self.upperGold = 20
        self.lvl = random.randint(1, player1.lvl) + 10


class NPC:
    def __init__(self, name):
        self.name = name

class Merchant(NPC, Player):
    def __init__(self, name, inv):
        super().__init__(name)
        self.inv = inv

    def showStock(self):
        print("\nHere's what I, %s, have for you today:" %self.name)
        sleep(2)
        print("\nSHOP")
        print("----")
        for item in self.inv:
            print("\n*%s" %item)
            item.info()

    def options(self, player):
        choice = 0
        while choice != '3':
            print("\nWhat would you like to do?")
            choice = input("[1]Buy \n[2]Sell \n[3]Leave \nEnter Choice: ")

            if choice == '1':
                itemName = input("\nWhat would you like to buy? ")
                try:
                    item = self.itemSearch(itemName)
                    if player.cash >= item.price:
                        player.buyItem(item, self)
                    else:
                        print("\nSorry pal, it appears you do not have enough gold to buy this item.")

                except (ValueError, AttributeError):
                    print("Opa! You seem to be talking about an item which I do not have!")


            elif choice == '2':
                player.checkInventory()
                itemName = input("\nWhat would you like to sell? ")
                try:
                    item = player.itemSearch(itemName)
                    player.sellItem(item, self)
                except (ValueError, AttributeError):
                    print("Uh oh! I don't think you have that item!")


            elif choice == '3':
                print("\nPleasure doing business with ya, %s." %player.name)
                sleep(1)

            else:
                print("\nSorry, I didn't quite get that.")
                sleep(0.5)

class Druid(Merchant):
    def __init__(self):
        self.name = "Elven Druid"
        self.inv = [jarHoney]

    def intro(self):
        print("\n     ED: Hello adventurer. For your brave struggles,\n         I offer you access to the fountain of youth.")

    def optionsIntro(self, player):
        self.intro()
        sleep(2)
        choice = 0
        while choice != '3':
            choice = input("\n[1]Get Healed to Full Health \n[2]Enter Shop \n[3]Leave \nChoice: ")
            if choice == '1':
                player.hp = player.maxHp
                sleep(0.5)
                print("\nYour health has been restored!")
                sleep(1)
            elif choice == '2':
                self.showStock()
                self.options(player)
            elif choice == '3':
                print("\nGoodbye, %s." %player.name)

    def options(self, player):
        choice = 0
        while choice != '3':
            print("\nWhat would you like to do?")
            choice = input("[1]Buy \n[2]Sell \n[3]Leave \nEnter Choice: ")

            if choice == '1':
                itemName = input("\nWhat would you like to buy? ")
                try:
                    item = self.itemSearch(itemName)
                    if player.cash >= item.price:
                        player.buyItem(item, self)
                    else:
                        print("\nForgive me, but you do not have enough Gold to purchase my item.")

                except (ValueError, AttributeError):
                    print("Oh no. I do not believe that I have that item.")

            elif choice == '2':
                player.checkInventory()
                itemName = input("\nWhat would you like to sell? ")
                try:
                    item = player.itemSearch(itemName)
                    player.sellItem(item, self)
                except (ValueError, AttributeError):
                    print("I'm sorry adventurer, but I don't believe you have that item.")


            elif choice == '3':
                print("\nYour transactions will aid the forest, %s." %player.name)
                sleep(1)

            else:
                print("\nI'm sorry, my Elvish ears did not understand you.")
                sleep(1)

class Area:
    def __init__(self, name, player):
        self.name = name
        self.player = player

    def enter (self):
        print("%s has entered %s." %(self.player.name, self.name))


    def options(self):
        print("What would you like to do?")

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
        print("\n%s encountered the %s!" %(self.player.name, druid.name))
        sleep(0.5)
        choice = 0
        druid.optionsIntro(self.player)
        sleep(3)

    def druidEvent(self, eventOcc):
        if eventOcc == False:
            num = random.randint(1,7)
            if num == 1:
                self.druidEncounter()
                #print ("Returns a special", True)
                return True
        #print ("Returns a", eventOccured)
        return False

    def events(self, eventOcc):
        eventOccured = eventOcc
        if eventOccured == False:
            eventOccured = self.druidEvent(eventOccured)
        #print ("Returns", eventOccured)
        return eventOccured

class Caverns(Area):
    def __init__(self, player):
        self.name = "The Caverns"
        self.player = player
        self.bosses = []

    def chooseMonster(self):
        self.monsters = [CreatureDepths()]
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
        print("\n%s encountered the %s!" %(self.player.name, druid.name))
        sleep(0.5)
        choice = 0
        druid.optionsIntro(self.player)
        sleep(3)

    def druidEvent(self, eventOcc):
        if eventOcc == False:
            num = random.randint(1,7)
            if num == 1:
                self.druidEncounter()
                #print ("Returns a special", True)
                return True
        #print ("Returns a", eventOccured)
        return False

    def events(self, eventOcc):
        eventOccured = eventOcc
        if eventOccured == False:
            eventOccured = self.druidEvent(eventOccured)
        #print ("Returns", eventOccured)
        return eventOccured

class CreateMonster:
    def __init__(self):
        pass

    def createBat(self, items):
        newBat = Bat(items)
        return newBat

class Game:
    def __init__(self, player):
        self.player = player

    def engageBattle(self, battle):
        battle.battleLoop()

    def enterArea(self):
        newForest = Forest(player1)
        newForest.enter()
        self.player.enteredArea = True
        self.area = newForest

    def idle (self):
        self.eventOccured = False
        choice = 0
        while choice != '1' or choice != '4':
            #self.eventOccured = False
            if self.player.enteredArea == False:
                self.enterArea()
            sleep(0.5)

            self.eventOccured = self.area.events(self.eventOccured)
            self.randMerchEvent()
            self.crimsonEvent()

            sleep(0.5)
            print("\nWhat would you like to do?")
            choice = input("[1]Fight an enemy \n[2]Open Inventory  \n[3]Check Stats \n[4]Boss Fight\nEnter Choice: ")

            if choice == '3':
                self.player.displayStats()

            elif choice == '2':
                self.player.checkInventory()
                self.player.invOptions()

            elif choice == '1':
                sleep(0.5)
                areaBattle = Battle(self.player, self.area.chooseMonster())
                self.engageBattle(areaBattle)

            elif choice == '4':
                sleep(0.5)
                boss = self.area.chooseBoss()
                if boss:
                    bossBattle = Battle(self.player, boss)
                    sleep(0.5)
                    boss.oneLiner()
                    sleep(2)
                    self.engageBattle(bossBattle)
                    if boss.hp <= 0: #If player dies
                        self.area.bosses.append(boss)
                else:
                    sleep(0.5)
                    print("\nAll bosses in %s have been defeated!" %self.area.name)
                    sleep(1.5)
            else:
                print("Please enter a proper choice.")

    def merchantEncounter(self):
        names = ["Robert", "Bob", "Dervin", "Lucario"]
        randomName = names[random.randint(0, len(names) -1)]
        merchant = Merchant (randomName, [stick, elixirRecov])

        print("\n%s encountered %s the Merchant!" %(self.player.name, merchant.name))
        choice = 0
        while choice != '2':
            print("\nWhat will you do?")
            choice = input("[1]Talk \n[2]Leave \nEnter Choice: ")
            if choice == '1':
                merchant.showStock()
                merchant.options(self.player)

    def crimsonEncounter(self):
        goals = [crimFlag, goldHammer, goldSickle, redNation]
        communist = CrimsonCommunist()

        print("\n%s encountered the %s!" %(self.player.name, communist.name))
        sleep(0.5)
        choice = 0
        print("\n   CC: Hello my comrade. I need to see some patriotism \n       before you may journey onwards.")
        sleep(3)
        choice = input("\n[1]Fight \n[2]Give Item \nEnter Choice: ")
        if choice == '2':
            self.player.checkInventory()

            itemName = input("\n   CC: What would you like to give me? ")
            try:
                item = self.player.itemSearch(itemName)

                if item in goals:
                    sleep(1)
                    print("\n   CC: You may proceed.")
                    sleep(1)
                else:
                    sleep(1)
                    print("\n   CC: What is this garbage? You are not a true comrade!")
                    sleep(2.5)
                    choice = 1
            except (ValueError, AttributeError):
                #print("Uh oh! I don't think you have that item!")
                pass
        if choice != '2':
            specialBattle = Battle(self.player, communist)
            self.engageBattle(specialBattle)

    def crimsonEvent(self):
        if self.eventOccured == False:
            num = random.randint(1,10)
            if num == 1:
                self.eventOccured = True
                self.crimsonEncounter()

    def randMerchEvent(self):
        if self.eventOccured == False:
            num = random.randint(1,10)
            if num <= 3:
                self.eventOccured = True
                self.merchantEncounter()

#In-game objects
class Item:
    def __init__(self, name, rarity, effect = None):
        rarities = {-1: "Special", 0: "Garbage", 1:"Abyssmal", 2:"Basic", 3:"Common", 4:"Uncommon",
        5:"Rare", 6:"Very Rare", 7: "Limited", 8: "Godlike", 9: "Unique"}
        self.name = name
        self.rarityName = rarities[rarity]
        self.rarity = rarity
        self.price = 5 * rarity
        self.description = self.setDescription()
        self.effect = effect
        #if self.effect != None:
            #self.description += "   Effect: " + self.effect.description
        self.oneUse = False

    def __str__(self):
        return self.name

    def setDescription(self):
        description = "     Rarity: " + str(self.rarityName) + "   Price: " + str(self.price) + " G"
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

class Potion(Consumable):
    def __init__(self, name, rarity, effect):
        super().__init__(name, rarity, effect)


class Weapon(Item):
    def __init__(self, name, rarity, dmg, luck, effect = None):
        super().__init__(name, rarity, effect)
        self.dmg = dmg
        self.luck = luck
        self.description += "   Damage: " + str(self.dmg)
        if self.effect != None:
            self.description += "\n   Effect: " + self.effect.description



class Armor(Item):
    def __init__(self, name, rarity, defence, luck, effect = None):
        super().__init__(name, rarity, effect)
        self.effect = effect
        self.defence = defence
        self.luck = luck
        self.description += "   Defence: " + str(self.defence)
        if self.effect != None:
            self.description += "\n   Effect: " + self.effect.description




class Effect:
    def __init__(self, name, description, turns, amount, affects, rand = False):
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

    def mainEffect(self, eff, enemy = None):
        if eff == "heal":
            self.heal()
        elif eff == "dmg":
            self.dmg(enemy)
        elif eff == "dmginc":
            self.dmgIncrease(enemy)

    def heal(self):
        if self.rand:
            self.amount = random.randint(self.lower, self.upper)
            player1.hp += self.amount
        else:
            player1.hp += self.amount
        if player1.hp > player1.maxHp:
            player.hp = player1.maxHp
        print("\n%s's %s has healed them for %d damage. (%d turns remaining)" %(player1.name, self.name, self.amount, self.turnsLeft))

    def dmg(self, enemy):
        if self.rand:
            self.amount = random.randint(self.lower, self.upper)
            enemy.hp -= self.amount
        else:
            enemy.hp -= self.amount
        print("\n%s's %s delt %d damage to %s. (%d turns remaining)" %(player1.name, self.name, self.amount, enemy.name, self.turnsLeft))

    def dmgIncrease(self, enemy):
        originalDmg = player1.dmg
        player1.dmg = int(player1.dmg * self.amount)
        amt = player1.dmg
        print("\n%s's Max Damage has been amplified by %d through %s. (%d turns remaining)" %(player1.name, self.amount, self.name, self.turnsLeft))
        if self.turnsLeft == 0 or (enemy.hp - amt <= 0):
            player1.dmg = originalDmg
            print("Damage has been returned to normal (for the sake of the player).")




#Game Initialization

#Initializing Player

    #Player Starting Items
global fists
fists = Weapon("Fists", -1, 2, 0)

cloth = Armor("Torn Cloth", 0, 0, 0)



#Initializing items
global stick
stickName = "A Sharp Stick"
stickRarity = 1
stickDmg = 1

stick = Weapon(stickName, stickRarity, stickDmg, 0)

#General Consumables
burnDesc = "For 3 turns, the enemy takes 3 Damage."
burnEffect = Effect("Burning", burnDesc, 3, 3, 'enemy')
burnEffect.effectActivator = "dmg"

potFlames = Potion("Potion of Flames", 3, burnEffect)


regenDesc = "The player will be healed for 2-5 HP for 4 turns."
regenEffect = Effect("Regeneration", regenDesc, 4, 5, 'player', True)
regenEffect.setRandLimits(2,5)
regenEffect.effectActivator = "heal"

elixirRecov = Potion("Elixir of Recovery", 4, regenEffect)


#Bat Items
global claw, batBat, batWing, vampArmor
claw = Weapon("Small Claw", 2, 3, 0)

batBat = Weapon("The Bat Bat", 6, 10, 0)

batWing = Item("Bat Wing", 2)

vampArmor = Armor("Vampiric Sheath", 5, 4, 0)

#Serpent Items
global fang, eyeSerpent, vipBlade, snakeHide, vileVenom
fang = Item("Snake Fang", 2)
eyeSerpent = Item("Eye of the Serpent", 3)
vipBlade = Weapon("Viperous Blade", 4, 6, 0)
snakeHide = Armor("Snakeskin Hide", 3, 5, 0)

venomDesc = "Poisons the target for 4 Damage, lasting 1 turn."
venomEffect = Effect("Venom", venomDesc, 1, 4, 'enemy')
venomEffect.effectActivator = "dmg"
vileVenom = Potion("Vial of Venom", 4, venomEffect)

#Ant Army Items
global bottleAnts, deadAnt, giantPincers
bottleAnts = Item("Bottle of Ants", 4)
deadAnt = Item("Dead Ant", 1)
giantPincers = Weapon("Giant Pincers", 3, 3, 0)

#Dust Elemental Items
global elemSoul
elemSoul = Item("Elemental Soul", 3)

#Creature of the Depths Items
global organs, skull, slayerBeast, spikedPelt
organs = Item("Noxious Intestinal Organs", 0)
skull = Item("Fiendish Skull", 1)
slayerBeast = Weapon("Slayer of the Beast", 3, 7, 1)
spikedPelt = Armor("Spiked Pelt", 2, 4, 0)


#CRIMSON COMMUNIST Items
#Not meant to be rude or insulting, not meant to offend anyone
#Just thought that it would be an interesting NPC idea
global crimFlag, goldHammer, goldSickle, redNation, potFury
crimFlag = Item("Crimson Flag", 2)
goldHammer = Weapon("Golden Hammer", 7, 14, 0)
goldSickle = Weapon("Golden Sickle", 7, 15, 0)
redNation = Armor("The Red Nation", 6, 12, 0)

furyDesc = "The player’s next 3 attacks will deal x2 Damage."
furyEffect = Effect("Growing Rage", furyDesc, 4, 2, 'player')
furyEffect.effectActivator = "dmginc"

potFury = Potion("Potion of Fury", 5, furyEffect)

#TREANT Items
global timber, lumber, clubThorns, protector
timber = Item("Ghostly Timber", 4)
lumber = Item("Lumber", 1)
clubThorns = Weapon("Club of Thorns", 3, 7, 0)
protEffectDesc = "Once per battle, restore 3-7 HP."
protectorEffect = Effect("Essence of the Forest", protEffectDesc, 1, 7, 'player', True)
protectorEffect.setRandLimits(3,7)
protectorEffect.effectActivator = "heal"


protector = Armor("Woodlandian Protector", 4, 5, 0, protectorEffect)

#QUEEN BEE Items
global nectar, honeycomb, sting, jarHoney
nectar = Item("Candy-Coated Nectar", 2)
honeycomb = Item("Hulking Honeycomb", 1)
sting = Weapon("The Empress' Sting", 4, 8, 0)

sweetDesc = "Heals the player for 3-4 HP."
sweetEffect = Effect("Sweetness", sweetDesc, 1, 4, 'player', True)
sweetEffect.setRandLimits(3,4)
sweetEffect.effectActivator = "heal"
sweetEffect.oneUse = True

jarHoney = Potion("Jar of Luscious Honey", 3, sweetEffect)


playerHp = 30
global player1
player1 = Player(playerHp, fists, cloth)


#Initializing Potions
global hpPot, flamePot
#hpPot = Potion("Healing Potion", 2, heal(10))
#flamePot = Potion("Potion of Flames", 4, dmg(15, hjk))


#Initializing Actual Game Interface
newGame = Game(player1)


#Initializing Monsters
while 1:

    #global randomBat, randomSnake

    newGame.idle()
