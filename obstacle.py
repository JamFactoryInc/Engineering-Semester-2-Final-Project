from matplotlib import patches, pyplot
from random import randint


class Obstacle:
    w = 9; h = 9

    def __init__(self, x, y, plot):

        self.x = x
        self.y = y
        self.plot = plot
        self.sprite = patches.Rectangle((x, y), self.w, self.h, linewidth = 1, edgecolor = 'black', facecolor = 'blue')
        print (x)
        plot.add_patch(self.sprite)
