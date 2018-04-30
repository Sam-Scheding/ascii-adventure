import random
from math import floor, sqrt
from collections import defaultdict
import noise
import numpy as np
import logging

logger = logging.getLogger(__name__)

RADIUS = 128
STICKINESS = 0.5 # 0 <= x <= 1
VILLAGE_POS = (floor(RADIUS / 2), floor(RADIUS / 2))

BIOMES = {
    'Lake': 'Lake',
    'Forest': 'Forest',
    'Barrens': 'Barrens',
}

TILES = {
    'ROAD': '#',
    'BARRENS': ' ',
    'SEED': '.',    
    'HOME': 'H',
    'IRON_MINE': 'I',
    'COAL_MINE': 'C',
    'SULPHUR_MINE': 'S',
    'TREE': 'T',
    'FIELD': ',',
    'WATER': '~',
    'GROTTO': 'G',
    'CAVE': 'V',
    'TOWN': 'O',
    # 'CITY': 'Y',
    'OUTPOST': 'P',
    'SHIP': 'W',
    'BUILDING': 'B',
    'BATTLEFIELD': 'F',
    'SWAMP': 'M',
    'CACHE': 'U'
}

# Sum must equal 1
TILE_PROBS = {
    TILES['TREE']: 0.30,
    TILES['FIELD']: 0.00,
    TILES['BARRENS']: 0.50,
    TILES['WATER']: 0.20,
}

LANDMARKS = {
    
    TILES['OUTPOST']: {'num': 0, 'minRadius': 0, 'maxRadius': 0, 'scene': 'outpost', 'label': 'An&nbsp;Outpost'},
    TILES['IRON_MINE']: {'num': 1, 'minRadius': 5, 'maxRadius': 5, 'scene': 'ironmine', 'label': 'Iron&nbsp;Mine'},
    TILES['COAL_MINE']: {'num': 1, 'minRadius': 10, 'maxRadius': 10, 'scene': 'coalmine', 'label': 'Coal&nbsp;Mine'},
    TILES['SULPHUR_MINE']: {'num': 0, 'minRadius': 0, 'maxRadius': 0, 'scene': 'outpost', 'label': 'Sulphur&nbsp;Mine'},
    TILES['GROTTO']: {'num': 10, 'minRadius': 0, 'maxRadius': RADIUS * 1.5, 'scene': 'house', 'label': 'An&nbsp;Old&nbsp;House'},
    TILES['CAVE']: {'num': 5, 'minRadius': 3, 'maxRadius': 10, 'scene': 'cave', 'label': 'A&nbsp;Cave'},
    TILES['TOWN']: { 'num': 10, 'minRadius': 10, 'maxRadius': 20, 'scene': 'town', 'label': 'An&nbsp;Abandoned&nbsp;Town' },
    # TILES['CITY']: { 'num': 20, 'minRadius': 20, 'maxRadius': RADIUS * 1.5, 'scene': 'city', 'label': 'A&nbsp;Ruined&nbsp;City' },
    TILES['SHIP']:{ 'num': 1, 'minRadius': 28, 'maxRadius': 28, 'scene': 'ship', 'label': 'A&nbsp;Crashed&nbsp;Starship'},
    # TILES['BOREHOLE']: { 'num': 10, 'minRadius': 15, 'maxRadius': RADIUS * 1.5, 'scene': 'borehole', 'label': 'A&nbsp;Borehole'},
    TILES['BATTLEFIELD']: { 'num': 5, 'minRadius': 18, 'maxRadius': RADIUS * 1.5, 'scene': 'battlefield', 'label': 'A&nbsp;Battlefield'},
    TILES['SWAMP']: { 'num': 1, 'minRadius': 15, 'maxRadius': RADIUS * 1.5, 'scene': 'swamp', 'label': 'A&nbsp;Murky&nbsp;Swamp'},
}

CITIES = {
    'RADIUS_MIN': 4,
    'RADIUS_MAX': 12,
    'NUM_CITIES': 10,
}


class World():

    def __init__(self):

        self.radius = RADIUS
        self.message = ""
        self.seed = None
        self.rep = None
        self.cities = None


    def new(self, seed):
        self.seed = seed
        random.seed(a=self.seed)
        # self.generate()

    def load(self, saved, seed):
        self.seed = seed
        random.seed(a=self.seed)
        self.rep = saved['rep']
        self.cities = saved['cities']  # Store the coords of cities separate from rep so we know where they are without having to check the rep


    def walkable(self, tile):

        if tile.icon in [TILES['BUILDING'], TILES['WATER']]:
            return False
        return True 

    def near(self, x_1, y_1, x_2, y_2, radius):
        mult = 4
        return x_2 - (radius * mult) < x_1 < x_2 + (radius * mult) and y_2 - (radius * mult) < y_1 < y_2 + (radius * mult)

    # Events set self.message
    def getMessage(self, player):   

        return self.message

    # Simulates erosion
    def decay(self, tile, x, y, radius, prev_tile):

        # get the distance from the current square to the center of the city
        x_dist = (x - radius) * (x - radius) * 2
        y_dist = (y - radius) * (y - radius) * 2
        dist = int(sqrt(x_dist + y_dist))  # Distance from the center of the city
        noise = random.randint(0, radius)
        """
            This implicitely creates a 2D array that looks like:
                323
                212
                323
            
        The array, coupled with the noise, makes it less likely that a building will decay 
        the closer they are to the city center 
        """
        if dist + noise < (13 * radius / 10):  # pseudo-Gaussian random probability distribution to decay the tile to what it was before we overlayed the city
            return TILES['BUILDING']
        return prev_tile


    """
        player_x, player_y must be absolute coordinates of the player
    """
    def proceduralView(self, radius, player_x, player_y):
        view = ''
        spacer = ' '
        for x in range(player_x - radius, player_x + radius + 1):
            for y in range(player_y - radius, player_y + radius + 1):
                tile = Tile(x, y, self.seed)
                if x == player_x and y == player_y:
                    tile.icon = '@'

                view += tile.icon + spacer
            view += '\n'

        return view


class Tile(object):

    def __init__(self, x, y, seed):

        self.x = x
        self.y = y
        self.seed = "{}{}{}".format(seed, self.x, self.y)
        random.seed(self.seed)
        self.biome = None
        self.icon = None
        self.message = ""
        self.perlinTerrain()
        self.perlinCity()

    def perlinCity(self):

        scale = random.randint(1, 100)
        # scale = 100.0
        octaves = 1
        persistence = 1
        lacunarity = 0.5
        kwargs = {
            'octaves': octaves, 
            'persistence': persistence, 
            'lacunarity': lacunarity, 
            'repeatx': 10, 
            'repeaty': 10, 
            'base': 0,
        }

        noise_val = noise.pnoise2(self.x / scale, self.y / scale, **kwargs)
        if self.x % 3 != 0 and self.y % 3 != 0:  # create buildings in a Manhattan grid
            self.tile = TILES['BUILDING']        

    def perlinTerrain(self):

        scale = random.randint(1, 100)
        scale = 100.0
        octaves = 6
        persistence = 2
        lacunarity = 1.5
        kwargs = {
            'octaves': octaves, 
            'persistence': persistence, 
            'lacunarity': lacunarity, 
            'repeatx': 10, 
            'repeaty': 10, 
            'base': 0,
        }

        if self.x == 0 and self.y == 0:
            self.icon = TILES['HOME']
            self.message = 'Home...'
            return
        noise_val = noise.pnoise2(self.x / scale, self.y / scale, **kwargs)
        if noise_val < -0.4:
            self.biome = BIOMES['Lake']
            self.icon = TILES['WATER']
            self.message = 'You cannot swim.'

        elif noise_val < 0.0:
            self.biome = BIOMES['Barrens']
            if random.randint(0, 100) < 1:
                self.icon = TILES['SEED']
                self.message = "A seed. Do you want to pick it up?"
            else:
                self.icon = TILES['BARRENS']

        elif noise_val < 0.5:
            self.biome = BIOMES['Forest']
            self.icon = TILES['TREE']
        else:
            self.biome = BIOMES['Barrens']
            self.icon = TILES['BARRENS']

