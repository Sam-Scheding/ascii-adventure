from curses import wrapper
import curses
import time, sys
from game import Game
from window import Window
import logging
import random
import uuid
logging.basicConfig(filename="out.log", level=logging.DEBUG, format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def main(stdscr):

	# seed = str(uuid.uuid4())
    game = Game()
    game.load()
    height, width = stdscr.getmaxyx()
    window = Window(height, width)
    stdscr.refresh()

    # game.reminisce(window)  # Show the players previous moves

    while True:

        world = game.world
        player = game.player
        view = world.getView(window.getMapRadius(), player)
        player.pickUp(world.getItem(player.x, player.y))
        player.getOlder()

        kwargs = {
            'map_view': view, 
            'message': world.getMessage(player), 
            'player': player, 
        }

        window.update(**kwargs)
        curses.flushinp()
        action = stdscr.getch()
        game.step(action, window, delay=player.tiredness)
        game.save(action)
        height, width = window.fitScreen(height, width, stdscr) # If the user has resized the terminal, we need to re fit everything




if __name__ == '__main__':

    wrapper(main)


