from curses import wrapper
import curses
import time, sys
from game import Game
from window import Window
import logging
from keyboard import KeyBoard
logging.basicConfig(filename="out.log", level=logging.DEBUG, format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def main(stdscr):

    game = Game(load=True)
    height, width = stdscr.getmaxyx()
    window = Window(height, width)
    stdscr.refresh()

    game.reminisce(window)  # Load the players previous moves

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

        elif KeyBoard.newGame(action):
            window.showLoading()
            game = Game(load=False)

        elif KeyBoard.exit(action):
            window.close()
            sys.exit(0)    


        game.save(action)


        height, width = window.fitScreen(height, width, stdscr) # If the user has resized the terminal, we need to re fit everything




if __name__ == '__main__':

    wrapper(main)


