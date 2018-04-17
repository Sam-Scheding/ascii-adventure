import curses
import textwrap
from math import floor, ceil

VIEW_RADIUS = 16

MAP_HEIGHT = VIEW_RADIUS * 2 + 2
MAP_WIDTH = VIEW_RADIUS * 4

INFO_WIDTH = 80
INFO_HEIGHT = 33
INFO_POS_X = MAP_WIDTH + 3
INFO_POS_Y = 1

LOG_WIDTH = 58
LOG_HEIGHT = INFO_HEIGHT - 2

STATS_WIDTH = 20
STATS_HEIGHT = 10
STATS_POS_X = MAP_WIDTH + LOG_WIDTH + 4 

INV_POS_X = MAP_WIDTH + LOG_WIDTH + 4
INV_POS_Y = STATS_HEIGHT + 2
INV_WIDTH = STATS_WIDTH
INV_HEIGHT = INFO_HEIGHT - STATS_HEIGHT - 2

class Window(object):

    def __init__(self, height, width):

        self.VIEW_RADIUS = VIEW_RADIUS

        curses.noecho()  # don't print entered characters
        curses.cbreak()  # Read keys without waiting for <enter>
        curses.curs_set(0)  # Hide the caret

        self.main_window = curses.newwin(height, width, 0, 0)
        self.map = Map(parent=self.main_window)
        self.info_box = InfoBox(parent=self.main_window) 

    def update(self, **kwargs):

        self.map.update(kwargs['map_view'])
        self.info_box.update(kwargs['message'], kwargs['player_pos'], kwargs['inventory'])
        self.main_window.refresh()

    def close(self):

        curses.nocbreak()
        curses.echo()
        curses.endwin()


class Map(object):
    def __init__(self, parent=None):
        super(Map, self).__init__()

        if parent:
            self.map_window = parent.subwin(MAP_HEIGHT + 2, MAP_WIDTH + 2, 0, 1)
            self.map_window.refresh()

    def update(self, view):
        if view:
            self.map_window.addstr(1, 0, view)
            # Show player icon in the middle of the view
            self.map_window.addstr(int(MAP_HEIGHT / 2), int(MAP_WIDTH / 2), '@')
            self.map_window.refresh()


class InfoBox(object):
    """docstring for Info"""
    def __init__(self, parent=None):
        super(InfoBox, self).__init__()
        if parent:
            self.container = parent.subwin(INFO_HEIGHT, INFO_WIDTH, INFO_POS_Y, INFO_POS_X)
            self.stats = self.container.subwin(STATS_HEIGHT, STATS_WIDTH, 2, STATS_POS_X)
            self.message_log = self.container.subwin(LOG_HEIGHT, LOG_WIDTH, 2, MAP_WIDTH + 4)
            self.inventory = self.container.subwin(INV_HEIGHT, INV_WIDTH, INV_POS_Y, INV_POS_X)

    def write(self, window, message, columns):

        rows = int(ceil(len(message) / columns))
        for row in range(1, rows + 1):
            window.addstr(row, 1, message[(row * columns) - columns:row * columns])


    def update(self, message, player_pos, inventory):

        self.message_log.clear()
        if message:
            self.write(self.message_log, message, LOG_WIDTH - 2)
        self.message_log.border()


        if player_pos:
            self.stats.clear()
            self.stats.addstr(1, 1, "Compass: {}-{}".format(player_pos[0], player_pos[1]))
            self.stats.addstr(2, 1, "Weather: Cold")

        self.stats.border()
        self.stats.refresh()


        self.inventory.clear()
        self.inventory.addstr(1, 1, "Inventory:")
        for line, item in enumerate(inventory):
            self.inventory.addstr(line + 2, 1, item)

        self.inventory.refresh()
        self.inventory.border()

        self.message_log.refresh()
        self.message_log.border()

        self.container.refresh()
        self.container.border()
