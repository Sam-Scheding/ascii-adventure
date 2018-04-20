from curses import wrapper
import curses
import time, sys
from world import World
from player import Player
from keyboard import KeyBoard
from window import Window
import logging

logging.basicConfig(filename="out.log", level=logging.DEBUG, format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def main(stdscr):

    
    height, width = stdscr.getmaxyx()
    window = Window(height, width)
    world = World()
    player = Player()
    stdscr.refresh()

    while True:

        view = world.getView(window.getMapRadius(), (player.x, player.y))
        player.pickUp(world.getItem(player.x, player.y))
        player.doTurn()
        kwargs = {
            'map_view': view, 
            'message': world.getMessage(player), 
            'player': player, 
        }

        window.update(**kwargs)

        time.sleep(player.tiredness)
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

        height, width = window.fitScreen(height, width, stdscr)

    window.close()

if __name__ == '__main__':

    wrapper(main)


