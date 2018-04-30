import random
from math import floor, sqrt
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

RADIUS = 128
STICKINESS = 0.5 # 0 <= x <= 1
VILLAGE_POS = (floor(RADIUS / 2), floor(RADIUS / 2))


TILES = {
    'ROAD': '#',
    'BARRENS': ' ',
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
        self.generate()

    def load(self, saved, seed):
        self.seed = seed
        random.seed(a=str(self.seed))
        self.rep = saved['rep']
        self.cities = saved['cities']  # Store the coords of cities separate from rep so we know where they are without having to check the rep

    def generate(self):
        # self.genTerrain()
        self.genCities()

    # def genTerrain(self):

    #     # Create a 2D array with the correct dimensions 
    #     self.rep = [[TILES['BARRENS'] for x in range(self.radius * 2 + 1)] for y in range(self.radius * 2 + 1)]
    #     # The Village is always at the exact center
    #     self.rep[self.radius][self.radius] = TILES['HOME']

    #     # Spiral out from there
    #     for r in range(1, self.radius + 1):
    #         for t in range(0, r * 8):

    #             if t < 2 * r:
    #                 x = self.radius - r + t
    #                 y = self.radius - r
    #             elif t < 4 * r:
    #                 x = self.radius + r
    #                 y = self.radius - (3 * r) + t
    #             elif t < 6 * r:
    #                 x = self.radius + (5 * r) - t
    #                 y = self.radius + r
    #             else:
    #                 x = self.radius - r
    #                 y = self.radius + (7 * r) - t

    #             self.rep[x][y] = self.chooseTile(x, y)


        for key, landmark in LANDMARKS.items():
            for l in range(0, landmark['num']):
                self.placeLandmark(landmark['minRadius'], landmark['maxRadius'], key)


    def genCities(self):

        # Generate cities at random coordinates
        for city in range(0, CITIES['NUM_CITIES'] + 1):

            # choose a location that won't overwrite the player's house
            city_radius = random.randint(CITIES['RADIUS_MIN'], CITIES['RADIUS_MAX'] + 1)
            x_choice = random.choice([(0, (self.radius - (city_radius * 2 + 1))), (self.radius + 1, (self.radius * 2) - (city_radius * 2 + 1))])
            y_choice = random.choice([(0, (self.radius - (city_radius * 2 + 1))), (self.radius + 1, (self.radius * 2) - (city_radius * 2 + 1))])
            x = random.randint(*x_choice)
            y = random.randint(*y_choice)
            self.generateCity(x, y, city_radius)  # Change this to return a list of buildings so we can load them again later
            self.cities += [{'x': x, 'y': y, 'radius': city_radius }]




    # def placeLandmark(self, minRadius, maxRadius, landmark):

    #     x = y = int(self.radius)

    #     while not self.isTerrain(self.rep[x][y]):

    #         r = floor(random.uniform(0, 1) * (maxRadius - minRadius)) + minRadius
    #         xDist = floor(random.uniform(0, 1) * r)
    #         yDist = r - xDist

    #         if random.uniform(0, 1) < 0.5:
    #             xDist = -xDist
    #         if random.uniform(0, 1) < 0.5:
    #             yDist = -yDist


    #         # Bound x and y into the map
    #         x = self.radius + xDist
    #         x = max(0, x)
    #         x = int(min(self.radius * 2, x))

    #         y = self.radius + yDist
    #         y = max(0, y)
    #         y = int(min(self.radius * 2, y))


    #     self.rep[x][y] = landmark



    def isTerrain(self, tile):
        return tile == TILES['WATER'] or tile == TILES['TREE'] or tile == TILES['BARRENS']

    def chooseTile(self, x, y):
        adjacent = [
            self.rep[x][y-1] if y > 0 else None,
            self.rep[x][y+1] if y < self.radius * 2 else None,
            self.rep[x+1][y] if x < self.radius * 2 else None,
            self.rep[x-1][y] if x > 0 else None
        ]

        chances = defaultdict(int)
        nonSticky = 1

        # If we are populating the area around the village, just return a TREE tile
        for i in adjacent:
            if i == TILES['HOME']:
                # Village must be in a TREE to maintain thematic consistency, yo.
                return TILES['TREE']
            elif i is not None:
                cur = i
                cur = (1 if type(cur) == int else 0)
                chances[i] = cur + STICKINESS
                nonSticky -= STICKINESS

        for name, tile in TILES.items():

            if self.isTerrain(tile):
                if tile in chances:
                    curr = 1
                else:
                    curr = 0
                curr += (TILE_PROBS[tile] * nonSticky)
                chances[tile] = curr

        l = [(key, chances[key]) for key in sorted(chances, key=chances.get, reverse=True)]
        c = 0
        r = random.uniform(0, 1)
        for item_chance in l:
            c += item_chance[1]
            if r < c:
                return item_chance[0]               
        
        return TILES['BARRENS']

    def walkable(self, x, y):
    
        # # If the player is trying to walk out of the map
        # if x > self.radius * 2 - 1 or y > self.radius * 2 - 1 or x < 0 or y < 0:
        #     self.message = 'You look ahead but there is nothing. You stop to take in the void.'
        #     return False


        # tile = self.getTile(x, y)
        tile = self.chooseTile(x, y)  # Procedural version of getTile()

        if tile == TILES['BUILDING']:
            self.message = 'A building. Do you want to <enter>?' 
            return False

        if tile == TILES['WATER']:
            self.message = 'You cannot swim.'
            return False

        if tile == TILES['HOME']:
            self.message = 'Home...'
            return True

        # If the player is near a city
        # for city in self.cities:
        #     if city['x'] <= x <= city['x'] + city['radius'] * 2 and city['y'] <= y <= city['y'] + city['radius'] * 2:
        #         self.message = "Ahead of you, a city slowly crumbles to dust."
        #         return True

        self.message = ""
        return True 

    def getTile(self, x, y):
        return self.rep[x][y] 

    def getItem(self, x, y):

        tile = self.getTile(x, y)
        if tile == TILES['TREE']:
            return 'Wood'
        return None

    # Events set self.message
    def getMessage(self, player):   

        return self.message

    def chooseTile(self, x, y, radius):

        # Simulates erosion
        def decay(tile, x, y, radius, prev_tile):

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

        if x == 0 and y == 0:
            return TILES['HOME']

        random.seed('{}{}{}'.format(self.seed, x, y))  # Generate a random seed specific to the tile so it's repeatable

        r = random.randint(1, 100)
        if r < 20:
            tile = TILES['TREE']
        else:
            tile = TILES['BARRENS']

        if x % 3 != 0 and y % 3 != 0:  # create buildings in a Manhattan grid
            for city in self.cities:
                if city['x'] - radius < x < city['x'] + radius and city['y'] - radius < y < city['y'] + radius:
                    tile = decay(TILES['BUILDING'], city['x'], city['y'], city['radius'], tile)

        return tile            

    """
        player_x, player_y must be absolute coordinates of the player
    """
    def proceduralView(self, radius, player_x, player_y):
        view = ''
        spacer = ' '
        for x in range(player_x - radius, player_x + radius + 1):
            for y in range(player_y - radius, player_y + radius + 1):
                if x == player_x and y == player_y:
                    view += '@' + spacer
                else:
                    view += self.chooseTile(x, y, radius) + spacer
            view += '\n'

        return view

    def generateCity(self, x_pos, y_pos, radius):

        # Simulates erosion
        def decay(tile, x, y, radius, prev_tile):

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
            if dist + noise > (13 * radius / 10):  # pseudo-Gaussian random probability distribution to decay the tile to what it was before we overlayed the city

                # If the city is in a TREE, only have trees on the edge of the city (looks nicer)
                if dist < radius:
                    tile = TILES['BARRENS']
                else:
                    tile = prev_tile
            return tile

        size = radius * 2 + 1

        for x in range(x_pos, x_pos + size):
            for y in range(y_pos, y_pos + size):

                prev_tile = self.rep[x][y]

                if x % 3 != 0 and y % 3 != 0:  # create buildings in a Manhattan grid
                    tile = TILES['BUILDING']
                else:
                    tile = self.rep[x][y]
                tile = decay(tile, x - x_pos, y - y_pos, radius, prev_tile)

                self.rep[x][y] = tile


    def getView(self, radius, player):

        x_lo = player.x - radius
        x_hi = player.x + radius
        y_lo = player.y - radius
        y_hi = player.y + radius
        left_space = right_space = bottom_space = 0
        rep = ''

        # Fill in the view for y < 0 with *
        if y_lo < 0:
            left_space = abs(0 - y_lo)              
            y_lo = 0

        # Fill in the view for y > radius * 2 with *
        elif y_hi > self.radius * 2 - 1:
            right_space = y_hi - (self.radius * 2)
            y_hi = self.radius * 2

        # Fill in the view for x > radius * 2 with *
        if x_hi > self.radius * 2 - 1:
            bottom_space = x_hi - (self.radius * 2 - 1)
            x_hi = self.radius * 2 - 1

        # Fill in the map for x < 0 with *
        while x_lo < 0:
            rep += ('  ' * (radius * 2)) + '\n' 
            x_lo += 1

        for x in range(x_lo, x_hi+1):
            rep += ('  ' * left_space)
            rep += ' '.join(map(str, self.rep[x][y_lo:y_hi]))
            rep += ('  ' * right_space)
            rep += '\n'

        while bottom_space > 0:
            rep += ('  ' * (radius * 2)) + '\n'
            bottom_space -= 1

        return rep


    def __str__(self):
        string_rep = ''
        for line in self.rep:
            for char in line:
                string_rep += char
            string_rep += '\n'
        return string_rep

