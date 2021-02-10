from matplotlib import pyplot
from random import randint, seed, random
from warehouse import Warehouse
from robot import Robot

seed(random())
plot = pyplot.subplots(1)[1]
zeros = [[255] * 174] * 224
plot.imshow(zeros, cmap = 'gray', vmin = 0, vmax = 255, origin = 'lower')
pyplot.ion(); pyplot.show()

warehouse = Warehouse(plot)


desiredBarcode = (0,0,0,2)
home = "a"

robot = Robot(plot, warehouse, home, desiredBarcode)

robot.patrol()