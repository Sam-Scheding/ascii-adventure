from world import World
from player import Player
from keyboard import KeyBoard
import json, time, sys
from collections import defaultdict
import logging
import random
import uuid

logger = logging.getLogger(__name__)

class Game(object):
    """docstring for Game"""
    def __init__(self):
        super(Game, self).__init__()
        self.keyboard = KeyBoard()        
        self.world = World()
        self.player = Player()
        self.seed = None

    def new(self):

        self.seed = str(uuid.uuid4())
        moves = open('moves.json', 'w')
        moves.write(str(list()))  # Write an empty list to moves.json
        self.world.new(self.seed)
        self.player.new(self.seed, x=self.world.radius, y=self.world.radius)

    def load(self):

        try:
            state = defaultdict(dict, json.load(open('state.json', 'r')))
            self.seed = state['seed']
            self.world.load(state['world'], self.seed)
            self.player.load(state['player'], self.seed)
        except FileNotFoundError as e:  # On the game's first run, the state and moves json wont exist, so just generate a new world and player
            self.new()



    def save(self, move):
        save_state = {
            'seed': self.seed,
            'player': {
                'x': self.player.x,
                'y': self.player.y,
                'turns': self.player.turns,
                'days': self.player.days,
                'tiredness': self.player.tiredness,
                'inventory': self.player.inventory.inventory,
            },
            'world': {
                'rep': self.world.rep,
                'cities': self.world.cities,
            },
        }

        json.dump(save_state, open("state.json", "w"))

        # Get the moves list from moves.json, append the new move, and then save it to moves.json again.
        try:
            moves = json.load(open('moves.json', 'r'))
        except FileNotFoundError as e:
            moves = []

        moves.append(move)
        json.dump(moves, open("moves.json", "w"))

    def getMoves(self):

        try:
            moves = json.load(open('moves.json', 'r'))
        except FileNotFoundError as e:
            moves = []
        return moves

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
