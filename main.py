import curses, time
from curses import wrapper
from math import floor
from world import World
from player import Player
from keyboard import KeyBoard

def main(stdscr):

    init()

    world = World()
    player = Player()
    view_radius = 16

    while True:

        view = world.getView(view_radius, (player.x, player.y))
        stdscr.addstr(0,0,view)

        # Show player icon in the middle of the view
        stdscr.addstr(view_radius, view_radius * 2, player.ICON)

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

    close()

def init():

    curses.noecho()  # don't print entered characters
    curses.cbreak()  # Read keys without waiting for <enter>
    curses.curs_set(0)  # Hide the caret

def close():

    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':

    wrapper(main)


