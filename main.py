from curses import wrapper
import curses
import time, sys
from game import Game
from window import Window
import logging
logging.basicConfig(filename="out.log", level=logging.DEBUG, format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def main(stdscr):

    game = Game()
    game.load()
    height, width = stdscr.getmaxyx()
    window = Window(height, width)
    stdscr.refresh()

    # game.reminisce(window)  # Show the players previous moves

    while True:

        world = game.world
        player = game.player
        view = world.proceduralView(window.getMapRadius(), player.x, player.y)
        player.getOlder()

        kwargs = {
            'map_view': view, 
            'message': player.getTileMessage(), 
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


