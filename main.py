import curses, time
from curses import wrapper
from world import World
from player import Player

def main(stdscr):

    init()

    world = World()
    player = Player()
    valid_input = True
    stdscr.addstr(str(world))

    while True:

        # Update the player's position
        stdscr.addstr(player.x, player.y, player.ICON)
        c = stdscr.getch()
        # Replace the tile that the player icon is currently covering
        feature = world.getFeatureAtLocation(player.x, player.y)
        stdscr.addstr(player.x, player.y, feature)
        
        if c == ord('w'):
            player.moveNorth()

        elif c == ord('a'):
            player.moveWest()

        elif c == ord('s'):
            player.moveSouth()

        elif c == ord('d'):
            player.moveEast()

        elif c == ord('q'):
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


