import curses, time
# import npyscreen
from curses import wrapper
from math import floor
from world import World, FEATURES
from player import Player
from keyboard import KeyBoard

VIEW_RADIUS = 16
MAP_HEIGHT = VIEW_RADIUS * 2 + 2
MAP_WIDTH = VIEW_RADIUS * 4

def main(stdscr):

    world = World()
    player = Player()

    curses.noecho()  # don't print entered characters
    curses.cbreak()  # Read keys without waiting for <enter>
    curses.curs_set(0)  # Hide the caret

    map_window = curses.newwin(MAP_HEIGHT + 2, MAP_WIDTH + 2, 0, 1)
    stdscr.refresh()
    stdscr.border(0)
    map_window.refresh()

    info_window = curses.newwin(20, 80, 1, MAP_WIDTH + 3)
    info_window.border()
    stdscr.refresh()
    info_window.refresh()

    while True:

        view = world.getView(VIEW_RADIUS, (player.x, player.y))
        map_window.addstr(1, 0, view)

        # Show player icon in the middle of the view
        map_window.addstr(int(MAP_HEIGHT / 2), int(MAP_WIDTH / 2), player.ICON)
        map_window.refresh()

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

        feature = world.getFeatureAtLocation(player.x, player.y)

        if world.atWorldEdge(player):
            info_window.clear()
            info_window.border()
            info_window.addstr(1, 2, 'You look ahead but there is nothing. The world stops.')

        if feature == FEATURES['HOUSE']:
            info_window.clear()
            info_window.border()
            info_window.addstr(1, 2, 'You come across a house.')


        stdscr.refresh()
        info_window.refresh()




    close()


def close():

    curses.nocbreak()
    curses.echo()
    curses.endwin()

if __name__ == '__main__':

    wrapper(main)


