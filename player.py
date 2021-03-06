import random
from inventory import Inventory
from math import floor
from world import Tile

class Player(object):

    ICON = '@'

    def __init__(self, seed=None):
        super(Player, self).__init__()

        self.turns_per_day = 7

    def new(self, seed):

        self.seed = seed
        random.seed(a=seed)
        self.x = 0
        self.y = 0
        self.tile = Tile(self.x, self.y, self.seed)
        self.turns = 0
        self.days = 0
        self.tiredness = 0  # 0.05
        self.inventory = Inventory()


    def load(self, state, seed):
        self.seed = seed
        self.x = state['x']
        self.y = state['y']
        self.tile = Tile(self.x, self.y, self.seed)
        self.turns = state['turns']
        self.days = state['days']
        self.tiredness = state['tiredness']
        self.inventory = Inventory(inventory=state['inventory'])

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

    def getTileMessage(self):
        return self.tile.message