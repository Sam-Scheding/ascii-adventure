from world import World
from player import Player
import json

class Game(object):
	"""docstring for Game"""
	def __init__(self):
		super(Game, self).__init__()
		self.new()

	def new(self):

	    self.world = World()
	    self.player = Player()
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
			},
			'inventory': self.player.inventory.inventory,
			'world': self.world.world_rep,
		}

		json.dump(save_state, open("state.json", "w"))
		moves = json.load(open('moves.json', 'r'))
		moves.append(move)
		json.dump(moves, open("moves.json", "w"))