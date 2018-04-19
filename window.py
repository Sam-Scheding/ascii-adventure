import curses
import textwrap, sys
from math import floor, ceil
import logging

logger = logging.getLogger(__name__)


class Window(object):

    def __init__(self, height, width):


        curses.noecho()  # don't print entered characters
        curses.cbreak()  # Read keys without waiting for <enter>
        curses.curs_set(0)  # Hide the caret
        self.height = height
        self.width = width
        self.window = curses.newwin(self.height, self.width, 0, 0)
        self.map = Map(parent=self.window)
        self.controls = Controls(parent=self)
        self.info = Info(parent=self) 

    def update(self, **kwargs):

        self.map.update(kwargs['map_view'])
        self.info.update(kwargs['message'], kwargs['player_pos'], kwargs['inventory'])
        self.window.refresh()

    def getMapRadius(self):
        return self.map.radius

    def close(self):

        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def write(self, window, message, columns):

        rows = int(ceil(len(message) / columns))
        for row in range(1, rows + 1):
            window.addstr(row, 1, message[(row * columns) - columns:row * columns])

class Map(object):
    def __init__(self, parent=None):
        super(Map, self).__init__()

        try:
            p_height, p_width = parent.getmaxyx()
            # Cascade all dimensions off of parent dimensions so it's not static and doesn't crash
        except Exception as e:
            logger.error('Parent window for Map not set: ', e)
            exit(1)

        self.width = int(p_width / 2 - 8)
        self.height = int(self.width / 2 + 4)  # width is stretch double, so we need to account for that
        self.radius = int(self.height / 2 - 2)  # This determines how much of the world to show the player
        logging.debug('h: {} w: {}'.format(self.height, self.width))
        self.window = parent.subwin(self.height, self.width, 0, 3)
        # self.window.border()
        self.window.refresh()


    def update(self, view):
        if view:
            self.window.addstr(1, 0, view)
            # Show player icon in the middle of the view
            self.window.addstr(floor(self.radius + 1), floor(self.radius * 2), '@')
            self.window.refresh()

class Controls(object):

    def __init__(self, parent=None):

        try:
            p_height, p_width = parent.window.getmaxyx()
        except Exception as e:
            logger.error('Parent window for Map not set: ', e)
            exit(1)

        # Cascade all dimensions off of parent dimensions so it's not static and doesn't crash
        self.width = int(p_width - 2)
        self.height = parent.height - parent.map.height + 2
        self.pos_y = parent.height - self.height
        self.pos_x = 1
        self.window = parent.window.subwin(self.height, self.width, self.pos_y, self.pos_x)
        self.window.border()
        self.window.refresh()


class Info(object):

    def __init__(self, parent=None):
        super(Info, self).__init__()

        try:
            p_height, p_width = parent.window.getmaxyx()
        except Exception as e:
            logger.error('Parent window for InfoBox not set: ', e)
            exit(1)

        self.width = int(p_width / 2)
        self.height = int(self.width / 2 - 4)
        self.pos_y = 1
        self.pos_x = parent.map.width + 4  # Shift the info box to the right by however wide the map is
        self.window = parent.window.subwin(self.height, self.width, self.pos_y, self.pos_x)
        self.window.border()
        self.messages = Messages(parent=self)
        self.stats = Stats(parent=self)
        self.inventory = Inventory(parent=self)



    def update(self, message, player_pos, inventory):

        # Call update() for all child windows
        self.messages.update(message)
        self.stats.update(player_pos)
        self.inventory.update(inventory)

        # Update self's window
        self.window.refresh()
        self.window.border()


class Inventory(object):

    def __init__(self, parent=None):
        super(Inventory, self).__init__()

        try:
            p_height, p_width = parent.window.getmaxyx()
        except Exception as e:
            logger.error('Parent window for Inventory not set: ', e)
            exit(1)

        self.height = int(p_height * 0.3 - 1)
        self.width = int(p_width - 2)
        self.pos_y = parent.pos_y + parent.messages.height + 1
        self.pos_x = parent.pos_x + 1
        self.window = parent.window.subwin(self.height, self.width, self.pos_y, self.pos_x)
        self.window.border()

    def update(self, inventory):

        self.window.clear()
        self.window.addstr(1, 1, "Inventory:")
        for line, item in enumerate(inventory):
            self.window.addstr(line + 2, 1, item)

        self.window.refresh()
        self.window.border()

class Stats(object):

    def __init__(self, parent=None):
        super(Stats, self).__init__()

        try:
            p_height, p_width = parent.window.getmaxyx()
        except Exception as e:
            logger.error('Parent window for Messages not set: ', e)
            exit(1)

        self.height = int(p_height * 0.5)
        self.width = int(p_width * 0.3)
        self.pos_y = parent.pos_y + 1
        self.pos_x = parent.pos_x + parent.messages.width + 1
        self.window = parent.window.subwin(self.height, self.width, self.pos_y, self.pos_x)
        self.window.border()

    def update(self, player_pos):

        if player_pos:
            self.window.clear()
            self.window.addstr(1, 1, "Compass: {}-{}".format(player_pos[0], player_pos[1]))
            self.window.addstr(2, 1, "Weather: Cold")

        self.window.border()
        self.window.refresh()


class Messages(object):

    def __init__(self, parent=None):
        super(Messages, self).__init__()

        try:
            p_height, p_width = parent.window.getmaxyx()
        except Exception as e:
            logger.error('Parent window for Messages not set: ', e)
            exit(1)
        self.height = int(p_height * 0.7)
        self.width = int(p_width * 0.7 - 1)
        self.pos_y = parent.pos_y + 1
        self.pos_x =  parent.pos_x + 1
        self.window = parent.window.subwin(self.height, self.width, self.pos_y, self.pos_x)
        self.window.border()

    def update(self, message):

        self.window.clear()
        if message:
            self.write(message, self.width - 2)

        self.window.refresh()
        self.window.border()

    def write(self, message, columns):

        rows = int(ceil(len(message) / columns))
        for row in range(1, rows + 1):
            self.window.addstr(row, 1, message[(row * columns) - columns:row * columns])
