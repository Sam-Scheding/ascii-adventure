"""
KeyBoard is a static class, that binds pey presses to actions
"""

import curses

class KeyBoard():

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
    def exit(key):
        return key in [curses.KEY_EXIT, ord('q')]
