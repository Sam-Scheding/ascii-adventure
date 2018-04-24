
TILES = {
    'FLOOR': ' ',
    'WALL_V': '|',
    'WALL_H': '-',
}
class Inside(object):

    def __init__(self):

        self.radius = 10
        self.rep = self.generate()


    def generate(self):
        
        size = self.radius * 2 + 1
        rep = [[TILES['FLOOR'] for x in range(0, size)] for y in range(0, size)]

        for row in range(0, size):
            for col in range(0, size):

                if row == 0 or row == size - 1:
                    rep[row][col] = TILES['WALL_H'] 

                elif col == 0 or col == size - 1:
                    rep[row][col] = TILES['WALL_V'] 

        return rep

    def getView(self):

        return str(self.generate())