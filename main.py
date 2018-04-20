from curses import wrapper
import curses
import time, sys
from game import Game
from keyboard import KeyBoard
from window import Window
import logging

logging.basicConfig(filename="out.log", level=logging.DEBUG, format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')

def main(stdscr):

    game = Game()
    height, width = stdscr.getmaxyx()
    window = Window(height, width)
    stdscr.refresh()

    while True:

        world = game.world
        player = game.player
        view = world.getView(window.getMapRadius(), player)
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

        elif KeyBoard.newGame(action):
            game.new()

        elif KeyBoard.exit(action):
            break

        height, width = window.fitScreen(height, width, stdscr) # If the user has resized the terminal, we need to re fit everything
        game.save(action)
    window.close()



if __name__ == '__main__':

    wrapper(main)


