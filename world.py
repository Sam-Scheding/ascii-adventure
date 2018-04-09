import random
from math import floor
from collections import defaultdict

WORLD_RADIUS = 15
STICKINESS = 0.5 # 0 <= x <= 1
VILLAGE_POS = (floor(WORLD_RADIUS / 2), floor(WORLD_RADIUS / 2))
FOOD_PER_MOVE = 2
WATER_PER_MOVE = 1
NORTH = (0, -1)
SOUTH = (0, 1)
WEST = (-1, 0)
EAST = (1, 0)


FEATURES = {
	'ROAD': '#',
	'BARRENS': '.',
	'VILLAGE': 'A',
	'IRON_MINE': 'I',
	'COAL_MINE': 'C',
	'SULPHUR_MINE': 'S',
	'FOREST': 'T',
	'FIELD': ',',
	'WATER': '~',
	'HOUSE': 'H',
	'CAVE': 'V',
	'TOWN': 'O',
	'CITY': 'Y',
	'OUTPOST': 'P',
	'SHIP': 'W',
	'BOREHOLE': 'B',
	'BATTLEFIELD': 'F',
	'SWAMP': 'M',
	'CACHE': 'U'
}

# Sum must equal 1
TILE_PROBS = {
	FEATURES['FOREST']: 0.30,
	FEATURES['FIELD']: 0.00,
	FEATURES['BARRENS']: 0.50,
	FEATURES['WATER']: 0.20,
}

LANDMARKS = {
	
	FEATURES['OUTPOST']: {'num': 0, 'minRadius': 0, 'maxRadius': 0, 'scene': 'outpost', 'label': 'An&nbsp;Outpost'},
	FEATURES['IRON_MINE']: {'num': 1, 'minRadius': 5, 'maxRadius': 5, 'scene': 'ironmine', 'label': 'Iron&nbsp;Mine'},
	FEATURES['COAL_MINE']: {'num': 1, 'minRadius': 10, 'maxRadius': 10, 'scene': 'coalmine', 'label': 'Coal&nbsp;Mine'},
	FEATURES['SULPHUR_MINE']: {'num': 0, 'minRadius': 0, 'maxRadius': 0, 'scene': 'outpost', 'label': 'Sulphur&nbsp;Mine'},
	FEATURES['HOUSE']: {'num': 10, 'minRadius': 0, 'maxRadius': WORLD_RADIUS * 1.5, 'scene': 'house', 'label': 'An&nbsp;Old&nbsp;House'},
	FEATURES['CAVE']: {'num': 5, 'minRadius': 3, 'maxRadius': 10, 'scene': 'cave', 'label': 'A&nbsp;Cave'},
	FEATURES['TOWN']: { 'num': 10, 'minRadius': 10, 'maxRadius': 20, 'scene': 'town', 'label': 'An&nbsp;Abandoned&nbsp;Town' },
	FEATURES['CITY']: { 'num': 20, 'minRadius': 20, 'maxRadius': WORLD_RADIUS * 1.5, 'scene': 'city', 'label': 'A&nbsp;Ruined&nbsp;City' },
	FEATURES['SHIP']:{ 'num': 1, 'minRadius': 28, 'maxRadius': 28, 'scene': 'ship', 'label': 'A&nbsp;Crashed&nbsp;Starship'},
	FEATURES['BOREHOLE']: { 'num': 10, 'minRadius': 15, 'maxRadius': WORLD_RADIUS * 1.5, 'scene': 'borehole', 'label': 'A&nbsp;Borehole'},
	FEATURES['BATTLEFIELD']: { 'num': 5, 'minRadius': 18, 'maxRadius': WORLD_RADIUS * 1.5, 'scene': 'battlefield', 'label': 'A&nbsp;Battlefield'},
	FEATURES['SWAMP']: { 'num': 1, 'minRadius': 15, 'maxRadius': WORLD_RADIUS * 1.5, 'scene': 'swamp', 'label': 'A&nbsp;Murky&nbsp;Swamp'},
}




class World():

	def __init__(self):

		self.RADIUS = WORLD_RADIUS
		self.world_rep = self.generate()

	def generate(self):

		# Create a 2D array with the correct dimensions 
		world_rep = [[FEATURES['BARRENS'] for x in range(self.RADIUS * 2 + 1)] for y in range(self.RADIUS * 2 + 1)]
		# The Village is always at the exact center
		world_rep[self.RADIUS][self.RADIUS] = FEATURES['VILLAGE']

		# Spiral out from there
		for r in range(1, self.RADIUS + 1):
			for t in range(0, r * 8):

				if t < 2 * r:
					x = self.RADIUS - r + t
					y = self.RADIUS - r
				elif t < 4 * r:
					x = self.RADIUS + r
					y = self.RADIUS - (3 * r) + t
				elif t < 6 * r:
					x = self.RADIUS + (5 * r) - t
					y = self.RADIUS + r
				else:
					x = self.RADIUS - r
					y = self.RADIUS + (7 * r) - t

				world_rep[x][y] = self.chooseTile(x, y, world_rep)


		for key, landmark in LANDMARKS.items():
			for l in range(0, landmark['num']):
				self.placeLandmark(landmark['minRadius'], landmark['maxRadius'], key, world_rep)

		return world_rep

	def placeLandmark(self, minRadius, maxRadius, landmark, world_rep):

		x = y = int(self.RADIUS)

		while not self.isTerrain(world_rep[x][y]):

			r = floor(random.uniform(0, 1) * (maxRadius - minRadius)) + minRadius
			xDist = floor(random.uniform(0, 1) * r)
			yDist = r - xDist

			if random.uniform(0, 1) < 0.5:
				xDist = -xDist
			if random.uniform(0, 1) < 0.5:
				yDist = -yDist


			# Bound x and y into the map
			x = self.RADIUS + xDist
			x = max(0, x)
			x = min(self.RADIUS * 2, x)

			y = self.RADIUS + yDist
			y = max(0, y)
			y = min(self.RADIUS * 2, y)


		world_rep[x][y] = landmark



	def isTerrain(self, tile):
		return tile == FEATURES['WATER'] or tile == FEATURES['FOREST'] or tile == FEATURES['BARRENS']

	def chooseTile(self, x, y, world_rep):
		adjacent = [
			world_rep[x][y-1] if y > 0 else None,
			world_rep[x][y+1] if y < self.RADIUS * 2 else None,
			world_rep[x+1][y] if x < self.RADIUS * 2 else None,
			world_rep[x-1][y] if x > 0 else None
		]

		chances = defaultdict(int)
		nonSticky = 1

		# If we are populating the area around the village, just return a forest tile
		for i in adjacent:
			if i == FEATURES['VILLAGE']:
				# Village must be in a forest to maintain thematic consistency, yo.
				return FEATURES['FOREST']
			elif i is not None:
				cur = i
				cur = (1 if type(cur) == int else 0)
				chances[i] = cur + STICKINESS
				nonSticky -= STICKINESS

		for name, tile in FEATURES.items():

			if self.isTerrain(tile):
				if tile in chances:
					curr = 1
				else:
					curr = 0
				curr += (TILE_PROBS[tile] * nonSticky)
				chances[tile] = curr

		l = [(key, chances[key]) for key in sorted(chances, key=chances.get, reverse=True)]
		c = 0
		r = random.uniform(0, 1)
		for item_chance in l:
			c += item_chance[1]
			if r < c:
				return item_chance[0] 				
		
		return FEATURES['BARRENS']

	def getFeatureAtLocation(self, x, y):
		return self.world_rep[x][y]	


	def __str__(self):
		string_rep = ''
		for line in self.world_rep:
			for char in line:
				string_rep += char
			string_rep += '\n'
		return string_rep

