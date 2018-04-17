import random
from math import floor
from collections import defaultdict

RADIUS = 100
STICKINESS = 0.5 # 0 <= x <= 1
VILLAGE_POS = (floor(RADIUS / 2), floor(RADIUS / 2))


FEATURES = {
    'ROAD': '#',
    'BARRENS': '.',
    'VILLAGE': 'H',
    'IRON_MINE': 'I',
    'COAL_MINE': 'C',
    'SULPHUR_MINE': 'S',
    'FOREST': 'T',
    'FIELD': ',',
    'WATER': '~',
    'GROTTO': 'G',
    'CAVE': 'V',
    'TOWN': 'O',
    'CITY': 'Y',
    'OUTPOST': 'P',
    'SHIP': 'W',
    'BOREHOLE': 'B',
    'BATTLEFIELD': 'F',
    'SWAMP': 'M',
    'CACHE': 'U'
}

MESSAGES = {
    
    FEATURES['VILLAGE']: 'Home...',
    FEATURES['GROTTO']: 'You stumble upon a grotto.',
}

# Sum must equal 1
TILE_PROBS = {
    FEATURES['FOREST']: 0.30,
    FEATURES['FIELD']: 0.00,
    FEATURES['BARRENS']: 0.50,
    FEATURES['WATER']: 0.20,
}

LANDMARKS = {
    
    FEATURES['OUTPOST']: {'num': 0, 'minRadius': 0, 'maxRadius': 0, 'scene': 'outpost', 'label': 'An&nbsp;Outpost'},
    FEATURES['IRON_MINE']: {'num': 1, 'minRadius': 5, 'maxRadius': 5, 'scene': 'ironmine', 'label': 'Iron&nbsp;Mine'},
    FEATURES['COAL_MINE']: {'num': 1, 'minRadius': 10, 'maxRadius': 10, 'scene': 'coalmine', 'label': 'Coal&nbsp;Mine'},
    FEATURES['SULPHUR_MINE']: {'num': 0, 'minRadius': 0, 'maxRadius': 0, 'scene': 'outpost', 'label': 'Sulphur&nbsp;Mine'},
    FEATURES['GROTTO']: {'num': 10, 'minRadius': 0, 'maxRadius': RADIUS * 1.5, 'scene': 'house', 'label': 'An&nbsp;Old&nbsp;House'},
    FEATURES['CAVE']: {'num': 5, 'minRadius': 3, 'maxRadius': 10, 'scene': 'cave', 'label': 'A&nbsp;Cave'},
    FEATURES['TOWN']: { 'num': 10, 'minRadius': 10, 'maxRadius': 20, 'scene': 'town', 'label': 'An&nbsp;Abandoned&nbsp;Town' },
    FEATURES['CITY']: { 'num': 20, 'minRadius': 20, 'maxRadius': RADIUS * 1.5, 'scene': 'city', 'label': 'A&nbsp;Ruined&nbsp;City' },
    FEATURES['SHIP']:{ 'num': 1, 'minRadius': 28, 'maxRadius': 28, 'scene': 'ship', 'label': 'A&nbsp;Crashed&nbsp;Starship'},
    FEATURES['BOREHOLE']: { 'num': 10, 'minRadius': 15, 'maxRadius': RADIUS * 1.5, 'scene': 'borehole', 'label': 'A&nbsp;Borehole'},
    FEATURES['BATTLEFIELD']: { 'num': 5, 'minRadius': 18, 'maxRadius': RADIUS * 1.5, 'scene': 'battlefield', 'label': 'A&nbsp;Battlefield'},
    FEATURES['SWAMP']: { 'num': 1, 'minRadius': 15, 'maxRadius': RADIUS * 1.5, 'scene': 'swamp', 'label': 'A&nbsp;Murky&nbsp;Swamp'},
}




class World():

    def __init__(self):

        self.RADIUS = RADIUS
        self.world_rep = self.generate()

    def generate(self):

        # Create a 2D array with the correct dimensions 
        world_rep = [[FEATURES['BARRENS'] for x in range(self.RADIUS * 2 + 1)] for y in range(self.RADIUS * 2 + 1)]
        # The Village is always at the exact center
        world_rep[self.RADIUS][self.RADIUS] = FEATURES['VILLAGE']

        # Spiral out from there
        for r in range(1, self.RADIUS + 1):
            for t in range(0, r * 8):

                if t < 2 * r:
                    x = self.RADIUS - r + t
                    y = self.RADIUS - r
                elif t < 4 * r:
                    x = self.RADIUS + r
                    y = self.RADIUS - (3 * r) + t
                elif t < 6 * r:
                    x = self.RADIUS + (5 * r) - t
                    y = self.RADIUS + r
                else:
                    x = self.RADIUS - r
                    y = self.RADIUS + (7 * r) - t

                world_rep[x][y] = self.chooseTile(x, y, world_rep)


        for key, landmark in LANDMARKS.items():
            for l in range(0, landmark['num']):
                self.placeLandmark(landmark['minRadius'], landmark['maxRadius'], key, world_rep)

        return world_rep

    def placeLandmark(self, minRadius, maxRadius, landmark, world_rep):

        x = y = int(self.RADIUS)

        while not self.isTerrain(world_rep[x][y]):

            r = floor(random.uniform(0, 1) * (maxRadius - minRadius)) + minRadius
            xDist = floor(random.uniform(0, 1) * r)
            yDist = r - xDist

            if random.uniform(0, 1) < 0.5:
                xDist = -xDist
            if random.uniform(0, 1) < 0.5:
                yDist = -yDist


            # Bound x and y into the map
            x = self.RADIUS + xDist
            x = max(0, x)
            x = min(self.RADIUS * 2, x)

            y = self.RADIUS + yDist
            y = max(0, y)
            y = min(self.RADIUS * 2, y)


        world_rep[x][y] = landmark



    def isTerrain(self, tile):
        return tile == FEATURES['WATER'] or tile == FEATURES['FOREST'] or tile == FEATURES['BARRENS']

    def chooseTile(self, x, y, world_rep):
        adjacent = [
            world_rep[x][y-1] if y > 0 else None,
            world_rep[x][y+1] if y < self.RADIUS * 2 else None,
            world_rep[x+1][y] if x < self.RADIUS * 2 else None,
            world_rep[x-1][y] if x > 0 else None
        ]

        chances = defaultdict(int)
        nonSticky = 1

        # If we are populating the area around the village, just return a forest tile
        for i in adjacent:
            if i == FEATURES['VILLAGE']:
                # Village must be in a forest to maintain thematic consistency, yo.
                return FEATURES['FOREST']
            elif i is not None:
                cur = i
                cur = (1 if type(cur) == int else 0)
                chances[i] = cur + STICKINESS
                nonSticky -= STICKINESS

        for name, tile in FEATURES.items():

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
        
        return FEATURES['BARRENS']

    def getFeatureAtLocation(self, x, y):
        return self.world_rep[x][y] 

    def getItem(self, x, y):

        feature = self.getFeatureAtLocation(x, y)
        if feature == FEATURES['FOREST']:
            return 'Wood'
        return None

    def atWorldEdge(self, obj):
    
        return obj.y >= self.RADIUS * 2 - 1 or obj.x >= self.RADIUS * 2 - 1 or obj.y <= 0 or obj.x <= 0

    def getMessage(self, player):   

        message = None

        # If the player is standing on something interesting
        feature = self.getFeatureAtLocation(player.x, player.y)
        if feature in MESSAGES:
            message = MESSAGES[feature]

        elif self.atWorldEdge(player):
            message = 'You look ahead but there is nothing. You stop to take in the void.'

        if not message:
            num = random.randint(0, 100)
            if num <= 5:  # 5% chance
                message = 'A wave of existential dread sweeps over you.'

        return message

    def getView(self, radius, pos):

        x_lo = pos[0] - radius
        x_hi = pos[0] + radius
        y_lo = pos[1] - radius
        y_hi = pos[1] + radius
        left_space = right_space = bottom_space = 0
        rep = ''

        # Fill in the view for y < 0 with *
        if y_lo < 0:
            left_space = abs(0 - y_lo)              
            y_lo = 0

        # Fill in the view for y > radius * 2 with *
        elif y_hi > self.RADIUS * 2 - 1:
            right_space = y_hi - (self.RADIUS * 2)
            y_hi = self.RADIUS * 2

        # Fill in the view for x > radius * 2 with *
        if x_hi > self.RADIUS * 2 - 1:
            bottom_space = x_hi - (self.RADIUS * 2 - 1)
            x_hi = self.RADIUS * 2 - 1

        # Fill in the map for x < 0 with *
        while x_lo < 0:
            rep += ('  ' * (radius * 2)) + '\n' 
            x_lo += 1

        for x in range(x_lo, x_hi+1):
            rep += ('  ' * left_space)
            rep += ' '.join(map(str, self.world_rep[x][y_lo:y_hi]))
            rep += ('  ' * right_space)
            rep += '\n'

        while bottom_space > 0:
            rep += ('  ' * (radius * 2)) + '\n'
            bottom_space -= 1

        return rep


    def __str__(self):
        string_rep = ''
        for line in self.world_rep:
            for char in line:
                string_rep += char
            string_rep += '\n'
        return string_rep

