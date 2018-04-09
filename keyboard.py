import curses

class KeyBoard():

	def up(key):
		return key in [curses.KEY_UP, ord('w')]

	def down(key):
		return key in [curses.KEY_DOWN, ord('s')]

	def left(key):
		return key in [curses.KEY_LEFT, ord('a')]

	def right(key):
		return key in [curses.KEY_RIGHT, ord('d')]

	def exit(key):
		return key in [curses.KEY_EXIT, ord('q')]
