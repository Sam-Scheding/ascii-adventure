from collections import defaultdict

class Inventory(object):

	def __init__(self, inventory=None):
		super(Inventory, self).__init__()

		if inventory != None:
			self.inventory = defaultdict(int, inventory)
		else:
			self.inventory = defaultdict(int)

	def add(self, item):
		self.inventory[item] += 1

	def remove(self, item):
		if self.inventory[item] > 0:
			self.inventory[item] -= 1
			return True
		return False

	def get(self):

		return sorted(["{}: {}".format(item, amount) for item, amount in self.inventory.items()])

	