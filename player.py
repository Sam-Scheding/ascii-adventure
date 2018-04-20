from world import RADIUS
from inventory import Inventory
from math import floor

class Player(object):

    ICON = '@'

    def __init__(self):
        super(Player, self).__init__()
        self.x = RADIUS
        self.y = RADIUS
        self.turns = 0
        self.days = 0
        self.days_per_year = 75
        self.turns_per_day = 7
        self.tiredness = 0.05
        self.inventory = Inventory()

    def getPosition(self):
        return (self.x, self.y)


    def moveNorth(self):
        if self.x > 0:
            self.x -= 1

    def moveSouth(self):
        if self.x < RADIUS * 2 - 1:
            self.x += 1

    def moveEast(self):
        if self.y < RADIUS * 2 - 1:
            self.y += 1

    def moveWest(self):
        if self.y > 0:
            self.y -= 1

    def pickUp(self, item):
        if item:
            self.inventory.add(item)
    
    def getInventory(self):
        return self.inventory.get()

    def doTurn(self):

        self.turns += 1

        self.days = floor(self.turns / self.turns_per_day)
