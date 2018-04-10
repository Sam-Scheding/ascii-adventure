from world import WORLD_RADIUS


class Player(object):

	ICON = '@'

	def __init__(self):
		super(Player, self).__init__()
		self.x = WORLD_RADIUS
		self.y = WORLD_RADIUS

	def getPosition(self):
		return (self.x, self.y)


	def moveNorth(self):
		if self.x > 0:
			self.x -= 1

	def moveSouth(self):
		if self.x < WORLD_RADIUS * 2 - 1:
			self.x += 1

	def moveEast(self):
		if self.y < WORLD_RADIUS * 2 - 1:
			self.y += 1

	def moveWest(self):
		if self.y > 0:
			self.y -= 1

