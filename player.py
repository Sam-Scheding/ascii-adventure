from world import RADIUS
from inventory import Inventory
from math import floor

class Player(object):

    ICON = '@'

    def __init__(self, state=None):
        super(Player, self).__init__()

        self.turns_per_day = 7

        if state != None:
            self.x = state['x']
            self.y = state['y']
            self.turns = state['turns']
            self.days = state['days']
            self.tiredness = state['tiredness']
            self.inventory = Inventory(inventory=state['inventory'])
        else:

            self.x = RADIUS
            self.y = RADIUS
            self.turns = 0
            self.days = 0
            self.tiredness = 0  # 0.05
            self.inventory = Inventory()

    def getPosition(self):
        return (self.x, self.y)


    def moveNorth(self):
        self.x -= 1

    def moveSouth(self):
        self.x += 1

    def moveEast(self):
        self.y += 1

    def moveWest(self):
        self.y -= 1

    def pickUp(self, item):
        if item:
            self.inventory.add(item)
    
    def getInventory(self):
        return self.inventory.get()

    def getOlder(self):

        self.turns += 1
        self.days = floor(self.turns / self.turns_per_day)
