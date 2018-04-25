"""
KeyBoard is a static class, that binds pey presses to actions
"""

import curses
from collections import defaultdict

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST =  (0,  1)
WEST = (0, -1)

SHIFT = {
    ord('w'): NORTH,
    ord('s'): SOUTH,
    ord('d'): EAST,
    ord('a'): WEST,
    curses.KEY_UP: NORTH,
    curses.KEY_DOWN: SOUTH,
    curses.KEY_LEFT: WEST,
    curses.KEY_RIGHT: EAST,
}

class KeyBoard():

    def getTransformation(self, key):
        shift = defaultdict(lambda: (0,0), SHIFT)
        return shift[key]

    @staticmethod 
    def up(key):
        return key in [curses.KEY_UP, ord('w')]

    @staticmethod 
    def down(key):
        return key in [curses.KEY_DOWN, ord('s')]

    @staticmethod 
    def left(key):
        return key in [curses.KEY_LEFT, ord('a')]

    @staticmethod 
    def right(key):
        return key in [curses.KEY_RIGHT, ord('d')]

    @staticmethod
    def enter(key):
        return key in [curses.KEY_ENTER]

    @staticmethod 
    def exit(key):
        return key in [17, b'^Q', ord('q')]

    @staticmethod 
    def newGame(key):
        return key in [14, b'^N']

