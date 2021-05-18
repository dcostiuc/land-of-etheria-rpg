from time import sleep
from items.globals import jarHoney


class NPC:
    def __init__(self, name):
        self.name = name


# include Player?
class Merchant(NPC):
    def __init__(self, name, inv):
        super().__init__(name)
        self.inv = inv

    def showStock(self):
        print("\nHere's what I, %s, have for you today:" % self.name)
        sleep(2)
        print("\nSHOP")
        print("----")
        for item in self.inv:
            print("\n*%s" % item)
            item.info()

    def options(self, player):
        choice = 0
        while choice != "3":
            print("\nWhat would you like to do?")
            choice = input("[1]Buy \n[2]Sell \n[3]Leave \nEnter Choice: ")

            if choice == "1":
                itemName = input("\nWhat would you like to buy? ")
                try:
                    item = self.itemSearch(itemName)
                    if player.cash >= item.price:
                        player.buyItem(item, self)
                    else:
                        print(
                            "\nSorry pal, it appears you do not have enough gold to buy this item."
                        )

                except (ValueError, AttributeError):
                    print(
                        "Opa! You seem to be talking about an item which I do not have!"
                    )

            elif choice == "2":
                player.checkInventory()
                itemName = input("\nWhat would you like to sell? ")
                try:
                    item = player.itemSearch(itemName)
                    player.sellItem(item, self)
                except (ValueError, AttributeError):
                    print("Uh oh! I don't think you have that item!")

            elif choice == "3":
                print("\nPleasure doing business with ya, %s." % player.name)
                sleep(1)

            else:
                print("\nSorry, I didn't quite get that.")
                sleep(0.5)


class Druid(Merchant):
    def __init__(self):
        self.name = "Elven Druid"
        self.inv = [jarHoney]

    def intro(self):
        print(
            "\n     ED: Hello adventurer. For your brave struggles,\n         I offer you access to the fountain of youth."
        )

    def optionsIntro(self, player):
        self.intro()
        sleep(2)
        choice = 0
        while choice != "3":
            choice = input(
                "\n[1]Get Healed to Full Health \n[2]Enter Shop \n[3]Leave \nChoice: "
            )
            if choice == "1":
                player.hp = player.maxHp
                sleep(0.5)
                print("\nYour health has been restored!")
                sleep(1)
            elif choice == "2":
                self.showStock()
                self.options(player)
            elif choice == "3":
                print("\nGoodbye, %s." % player.name)

    def options(self, player):
        choice = 0
        while choice != "3":
            print("\nWhat would you like to do?")
            choice = input("[1]Buy \n[2]Sell \n[3]Leave \nEnter Choice: ")

            if choice == "1":
                itemName = input("\nWhat would you like to buy? ")
                try:
                    item = self.itemSearch(itemName)
                    if player.cash >= item.price:
                        player.buyItem(item, self)
                    else:
                        print(
                            "\nForgive me, but you do not have enough Gold to purchase my item."
                        )

                except (ValueError, AttributeError):
                    print("Oh no. I do not believe that I have that item.")

            elif choice == "2":
                player.checkInventory()
                itemName = input("\nWhat would you like to sell? ")
                try:
                    item = player.itemSearch(itemName)
                    player.sellItem(item, self)
                except (ValueError, AttributeError):
                    print(
                        "I'm sorry adventurer, but I don't believe you have that item."
                    )

            elif choice == "3":
                print("\nYour transactions will aid the forest, %s." % player.name)
                sleep(1)

            else:
                print("\nI'm sorry, my Elvish ears did not understand you.")
                sleep(1)
