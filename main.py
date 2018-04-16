import curses, time, sys
# import npyscreen
from curses import wrapper
import textwrap
from math import floor, ceil
from world import World, FEATURES
from player import Player
from keyboard import KeyBoard

VIEW_RADIUS = 16
MAP_HEIGHT = VIEW_RADIUS * 2 + 2
MAP_WIDTH = VIEW_RADIUS * 4
TURN_WAIT = 0.03

LOG_WIDTH = 59
COMPASS_WIDTH = 18
world = World()
player = Player()

def main(stdscr):


    curses.noecho()  # don't print entered characters
    curses.cbreak()  # Read keys without waiting for <enter>
    curses.curs_set(0)  # Hide the caret

    map_window = curses.newwin(MAP_HEIGHT + 2, MAP_WIDTH + 2, 0, 1)
    stdscr.refresh()
    stdscr.border()

    info_window = stdscr.subwin(20, 80, 1, MAP_WIDTH + 3)
    info_window.border()
    compass = info_window.subwin(4, COMPASS_WIDTH, 2, MAP_WIDTH * 2)
    message_log = info_window.subwin(10, LOG_WIDTH, 2, MAP_WIDTH + 5)
    updateInfoWindow(compass, message_log)
    map_window.refresh()
    stdscr.refresh()

    while True:


        view = world.getView(VIEW_RADIUS, (player.x, player.y))
        map_window.addstr(1, 0, view)

        # Show player icon in the middle of the view
        map_window.addstr(int(MAP_HEIGHT / 2), int(MAP_WIDTH / 2), player.ICON)
        map_window.refresh()

        time.sleep(TURN_WAIT)
        curses.flushinp()
        action = stdscr.getch()


        if KeyBoard.up(action):
            player.moveNorth()

        elif KeyBoard.left(action):
            player.moveWest()

        elif KeyBoard.down(action):
            player.moveSouth()

        elif KeyBoard.right(action):
            player.moveEast()

        elif KeyBoard.exit(action):
            break

        updateInfoWindow(compass, message_log)
        info_window.refresh()  # Needs to happen after stdscr.refresh()
        compass.refresh()
        message_log.refresh()
        stdscr.refresh()
    close()


def updateInfoWindow(compass, message_log):

    message_log.clear()
    message = world.getMessage(player)
    if message:
        writeMessage(message_log, message, LOG_WIDTH - 2)
    message_log.border()

    compass.clear()
    writeMessage(compass, "Compass: {}-{}".format(player.x, player.y), COMPASS_WIDTH)
    compass.border()

def writeMessage(window, message, columns):

    rows = int(ceil(len(message) / columns))
    for row in range(1, rows + 1):
        window.addstr(row, 1, message[(row * columns) - columns:row * columns])

def close():

    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':

    wrapper(main)


