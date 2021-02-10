from matplotlib import patches, pyplot
from random import randint
from itertools import permutations
from box import Box
from obstacle import Obstacle

class Warehouse:
    _ = [0, 0, 0, 0, 1, 1, 1, 1]
    barcodes = list(set(permutations(_, 4)))
    boxes = []
    obstacles = []

    def __init__(self, plot):
        self.plot = plot
        y = -25

        for i in range(4):
            y += 50
            self.buildShelf(2, 25, y)
            self.buildShelf(2, 100, y)

            self.addObstacle(i, 0)
            self.addObstacle(i, 1)
            self.addObstacle(i, 2)


    def buildShelf(self, numBoxes, x, y):
        h = 25; w = 50

        self.plot.add_patch(patches.Rectangle((x, y), w, h, linewidth = 1, edgecolor = 'black', facecolor = 'gray'))
        box1 = Box(x + randint(0, w - 10), y, self.plot)
        box2 = Box(x + randint(0, w - 10), y + 16, self.plot)
        boxes = [box1, box2]
        self.boxes.extend(boxes)

    def addObstacle(self, r, c):

        obs = Obstacle(c*75 + randint(0,1)*11 + 2, r* 50 + 30, self.plot)
        
        self.obstacles.append(obs)

   