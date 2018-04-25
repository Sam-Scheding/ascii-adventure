from world import World
from player import Player
from keyboard import KeyBoard
import json, time, sys
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class Game(object):
    """docstring for Game"""
    def __init__(self, load=False):
        super(Game, self).__init__()
        self.keyboard = KeyBoard()
        if load == True:
            self.load()
        else:
            self.new()
            moves = open('moves.json', 'w')
            moves.write('[]')  # Prob a better way to do this with a default dict

    def new(self):
            self.world = World()
            self.player = Player()

    def load(self):

        try:
            state = defaultdict(dict, json.load(open('state.json', 'r')))
            self.world = World(rep=state['world']['rep'], cities=state['world']['cities'])
            self.player = Player(state=state['player'])
        except FileNotFoundError as e:  # On the game's first run, the state and moves json wont exist, so just generate a new world and player
            self.new()



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
            'world': {
                'rep': self.world.world_rep,
                'cities': self.world.cities,
            },
        }

        json.dump(save_state, open("state.json", "w"))

        # Get the moves list from moves.json, append the new move, and then save it to moves.json again.
        moves = json.load(open('moves.json', 'r'))
        moves.append(move)
        json.dump(moves, open("moves.json", "w"))

    def getMoves(self):

        return json.load(open('moves.json', 'r'))


    def reminisce(self, window):

        moves = self.getMoves()
        world = self.world
        player = self.player
        player.x = 100
        player.y = 100
        for action in moves:

            view = world.getView(window.getMapRadius(), player)
            window.update(map_view=view, player=player, message="You look back on your life and realise how little you have accomplished")
            self.step(action, reminisce=True, delay=0.006)


    def step(self, action, window, reminisce=False, delay=0):

        delta = self.keyboard.getTransformation(action)

        # I have no idea why this works
        walkable = self.world.walkable(self.player.x + delta[0], self.player.y + delta[1])

        if KeyBoard.up(action) and walkable:
            self.player.moveNorth()

        elif KeyBoard.left(action) and walkable:
            self.player.moveWest()

        elif KeyBoard.down(action) and walkable:
            self.player.moveSouth()

        elif KeyBoard.right(action) and walkable:
            self.player.moveEast()

        elif KeyBoard.enter(action):
            tile = self.world.getTile(self.player.x, self.player.y)
            next_tile = self.world.getTile(self.player.x + delta[0], self.player.y + delta[1])
            if tile == 'T':
                self.world.message = 'A tree'

        elif not reminisce and KeyBoard.newGame(action):
            window.showLoading()
            self.new()

        elif not reminisce and KeyBoard.exit(action):
            window.close()
            sys.exit(0)    

        time.sleep(delay)
