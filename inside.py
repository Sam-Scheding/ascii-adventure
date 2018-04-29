import random

TILES = {
    'FLOOR': ' ',
    'WALL_V': '|',
    'WALL_H': '-',
}

class Room(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width

class Inside(object):

    def __init__(self, ):
        super(Inside, self).__init__()
        self.block_dim = 4
        self.height = self.block_dim * 2
        self.width = self.block_dim * 4
        self.rep = self.generate()

    def generate(self):

        rep = []
        v_walls = []
        h_walls = []
        for y in range(0, self.height + 1):
            row = []
            for x in range(0, self.width + 1):
                if (y % self.block_dim == 0):
                    row += ['#']
                    if y != 0 and y != self.width:
                        h_walls += [(x, y)]
                elif (x % self.block_dim == 0):
                    row += ['#']
                    v_walls += [(x, y)]
                else:
                    row += [' ']

            rep += [row]

        # # Create the basic walls
        print(v_walls)
        print(h_walls)
        # Knock some walls out


        return rep


    def printa(self):

        for row in self.rep:
            for char in row:
                print(char, end='')
            print()


inside = Inside()
inside.printa()

