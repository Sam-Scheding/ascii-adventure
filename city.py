import random
from math import sqrt



def generate(radius):

	# Simulates erosion
	def decay(tile):

		# get the distance from the current square to the center of the city
		x_dist = (x - radius) * (x - radius) * 2
		y_dist = (y - radius) * (y - radius) * 2
		dist = int(sqrt(x_dist + y_dist)) 
		noise = random.randint(0, radius)
		"""
			This implicitely creates a 2D array that looks like:
				323
				212
				323
			
		The array, coupled with the noise, makes it less likely that a building will decay 
		the closer they are to the city center 
		"""
		if dist + noise > (13 * radius / 10):
			tile = '.'
		return tile

	size = radius * 2 + 1
	spacer = ' '

	for x in range(0, size):
		for y in range(0, size):

			if x % 3 != 0 and y % 3 != 0:  # create buildings in a manhatten grid
				tile = 'B'
			else: 
				tile = '.'

			tile = decay(tile)

			print('{}{}'.format(tile, spacer), end='')
		print('')


radius = random.randint(4, 12)

generate(radius)

