from world import World
from player import Player
from keyboard import KeyBoard
import json
from collections import defaultdict

class Game(object):
    """docstring for Game"""
    def __init__(self, load=False):
        super(Game, self).__init__()
        if load == True:
            self.load()
        else:
            self.world = World()
            self.player = Player()

    def load(self):
        state = defaultdict(dict, json.load(open('state.json', 'r')))
        self.world = World(rep=state['world'])
        self.player = Player(state=state['player'])
        moves = open('moves.json', 'w')
        moves.write('[]')


    def save(self, move):
        save_state = {
            'player': {
                'x': self.player.x,
                'y': self.player.y,
                'turns': self.player.turns,
                'days': self.player.days,
                'tiredness': self.player.tiredness,
                'inventory': self.player.inventory.inventory,
            },
            'world': self.world.world_rep,
        }

        json.dump(save_state, open("state.json", "w"))

        # Get the moves list from moves.json, append the new move, and then save it to moves.json again.
        moves = json.load(open('moves.json', 'r'))
        moves.append(move)
        json.dump(moves, open("moves.json", "w"))

    def getMoves(self):

        return json.load(open('moves.json', 'r'))




