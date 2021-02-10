from matplotlib import patches, pyplot
from random import randint
from itertools import permutations

_ = [0, 0, 0, 0, 1, 1, 1, 1]
barcodes = list(set(permutations(_, 4)))

class Box:
    w = 9; h = 9

    def __init__(self, x, y, plot):
        rand = randint(0, len(barcodes) - 1)
        self.barcode = barcodes.pop(rand)
        self.x = x
        self.y = y
        self.plot = plot
        self.sprite = patches.Rectangle((x, y), self.w, self.h, linewidth = 1, edgecolor = 'black', facecolor = 'black')
        plot.add_patch(self.sprite)

    def move(self, change):
        (dx, dy) = change
        self.x += dx; self.y += dy
        self.sprite.remove()
        self.sprite = patches.Rectangle((self.x, self.y), self.w, self.h, linewidth = 1, edgecolor = 'black', facecolor = 'black')
        self.plot.add_patch(self.sprite)

    def moveTimed(self, change):
        self.move(change)
        pyplot.pause(0.001)