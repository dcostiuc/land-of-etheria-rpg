class Area:
    def __init__(self, name, player):
        self.name = name
        self.player = player

    def enter(self):
        print("%s has entered %s." % (self.player.name, self.name))

    def options(self):
        print("What would you like to do?")
