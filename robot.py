from matplotlib import patches, pyplot
from warehouse import Warehouse
from math import sqrt

class Robot:
    def __init__(self, plot, warehouse, home, desiredBarcode):
        self.desiredBarcode = desiredBarcode
        self.sprite = None; self.box = None
        self.position = [9, 9] # x, y
        self.location = [0, 0] # row, col
        if(home == "a"):
            self.position = [9,9]
            self.location = [0, 0]
        elif(home == "b"):
            self.position = [159,9]
            self.location = [0, 2]
        elif(home == "c"):
            self.position = [9,209]
            self.location = [3, 0]
        elif(home == "d"):
            self.position = [159,209]
            self.location = [3, 2]
        self.size = (12, 7) # w, l
        self.widthUnit = 75; self.heightUnit = 50
        self.facing = 0
        self.right = True; self.left = False
        self.north = 0; self.east = 1; self.south = 2; self.west = 3
        self.topRight = (self.north, self.east)
        self.topLeft = (self.north, self.west)
        self.bottomRight = (self.south, self.east)
        self.bottomLeft = (self.south, self.west)
        self.collectedBoxes = [0,0,0,0,0]
        # self.corners = {
        #     self.topRight: [(0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1)],
        #     self.topLeft: [(0, 1, 1, 1), (0, 1, 1, 0), (0, 1, 0, 1), (0, 1, 0, 0)],
        #     self.bottomRight: [(1, 0, 0, 0), (1, 0, 1, 0), (1, 0, 1, 1), (1, 1, 1, 1)],
        #     self.bottomLeft: [(1, 1, 1, 0), (1, 0, 0, 1), (1, 1, 0, 1), (1, 1, 0, 0)]
        # }

        self.plot = plot
        self.warehouse = warehouse
        self.home = home

    # movement
    def fwd(self, dist, ignore = False):
        i = dist
        while i > 0:
            plot = self.plot
            sprite = self.sprite
            box = self.box
            (x, y) = self.position
            (w, l) = self.size
            facing = self.facing

            # north
            if not facing:
                y += 1

                if box:
                    box.move((0, 1))

            # east
            elif facing == 1:
                x += 1

                if box:
                    box.move((1, 0))

            # south
            elif facing == 2:
                y -= 1

                if box:
                    box.move((0, -1))

            # west
            elif facing == 3:
                x -= 1

                if box:
                    box.move((-1, 0))

            position = (x, y)
            self.position = position
            self.detectBox()
            if(not ignore):
                #print(ignore)
                i -= self.detectObstacle()
            (x, y) = self.position
            self.sprite = sprite = patches.Rectangle(position, l, w, linewidth = 1, edgecolor = 'black', facecolor = 'red')
            plot.add_patch(sprite)
            # pyplot.pause(0.001)
            pyplot.pause(0.001)
            sprite.remove()
            i -= 1
            #print(position)

    def rotate(self, d):
        box = self.box
        (w, l) = self.size
        facing = self.facing

        # right
        if d:
            facing = (facing + 1) % 4
            coords = ((0, 4), (4, -4), (-4, 0), (0, 0))

        # left
        else:
            facing = (facing - 1) % 4
            coords = ((-4, 4), (4, 0), (0, 0), (0, -4))

        if box:
            box.move(coords[facing])

        if not facing or facing == 2:
            l = 7; w = 12

        else: l = 12; w = 7

        self.size = (w, l)
        self.facing = facing

    def turn(self, d):
        i = 0
        right = self.right

        if not d:
            print('turning north')

        elif d == 1:
            print('turning east')

        elif d == 2:
            print('turning south')

        else:
            print('turning west')

        while self.facing != d:
            self.rotate(right)
            i += 1

        return i

    def moveTo(self, location, ignore = False):
        self.turn(location[0]); self.skip(4, ignore)
        self.turn(location[1]); self.skip(4, ignore)

    def goToCorner(self):
        box = self.box
        home = self.home
        if(home == "a"):
            self.moveTo(self.bottomLeft, True)
        elif(home  == "b"):
            self.moveTo(self.bottomRight, True)
        elif(home  == "c"): 
            self.moveTo(self.TopLeft, True)   
        elif(home  == "d"):        
            self.moveTo(self.TopRight, True)
        self.putDownBox()
        return
        # for location in self.corners:
        #     corner = self.corners[location]

        #     for barcode in corner:
        #         if box.barcode == barcode:
        #             print('going to corner', location)
        #             self.moveTo(location, True)
        #             self.putDownBox()
        #             return

    def prevBox(self):
        (row, col) = self.location
        (brow, bcol) = self.boxLocation
        north = self.north; east = self.east; south = self.south; west = self.west

        # move to row
        if not self.location[0]:
            self.turn(north)

        else: self.turn(south)
        skipNum = abs(row - brow)
        if (self.collectedBoxes[brow] == 2 and not brow) or self.collectedBoxes[brow] == 4:
            skipNum = abs(row - brow)
        self.skip(skipNum)

        # move to col
        if not self.location[1]:
            self.turn(east)

        else: self.turn(west)
        self.skip(2)

    def patrol(self):
        north = self.north; east = self.east; west = self.west; south = self.south

        print("patrolling")
        if not self.location[1]:
            self.turn(east)

        else: self.turn(west)

        for _ in range(5):
            self.skip(2)
            if(self.home == "a" or self.home == "b"):
                self.turn(north)
            elif(self.home == "c" or self.home == "d"):
                self.turn(south)
            self.skip()

            if not self.location[1]:
                self.turn(east)

            else: self.turn(west)

    def skip(self, n = 1, ignore = False):
        heightUnit = self.heightUnit; widthUnit = self.widthUnit
        facing = self.facing
        print('skipping %i' % n)

        for _ in range(n):
            (row, col) = self.location

            if row < 4 and not facing:
                self.fwd(heightUnit)
                row += 1

            elif row > 0 and facing == 2:
                self.fwd(heightUnit)
                row -= 1

            elif col > 0 and facing == 3:
                self.fwd(widthUnit)
                col -= 1

            elif col < 2 and facing == 1:
                self.fwd(widthUnit)
                col += 1

            self.location = (row, col)

            if not ignore and self.box:
                print('ignore')
                self.goToCorner()
                self.prevBox()
                break

        else: return

        if ignore:
            self.patrol()

    # box
    def scan(self, box):
        print("scanning box")
        print(box.barcode)
        return box.barcode

    def detectBox(self):
        plot = self.plot
        warehouse = self.warehouse
        (x, y) = self.position
        right = self.right; left = self.left
        north = self.north; south = self.south

        if not self.box:
            for box in warehouse.boxes:
                if box.x == x - 1:
                    if box.y == y + 16:
                        n = self.turn(north)
                        self.fwd(3)
                        (w, l) = self.size
                        self.sprite = sprite = patches.Rectangle(self.position, l, w, linewidth = 1, edgecolor = 'black', facecolor = 'red')
                        plot.add_patch(sprite)
                        (x, y) = self.position
                        self.pickUpBox(box)
                        sprite.remove()
                        self.rotate(right); self.rotate(right)
                        self.fwd(3)

                        for _ in range(n):
                            self.rotate(right)

                    elif box.y == y - 18:
                        n = self.turn(south)
                        self.fwd(9)
                        (w, l) = self.size
                        self.sprite = sprite = patches.Rectangle(self.position, l, w, linewidth = 1, edgecolor = 'black', facecolor = 'red')
                        plot.add_patch(sprite)
                        (x, y) = self.position
                        self.pickUpBox(box)
                        sprite.remove()
                        self.rotate(left); self.rotate(left)
                        self.fwd(9)

                        for _ in range(n):
                            self.rotate(right)

    def detectObstacle(self):
        plot = self.plot
        warehouse = self.warehouse
        (x, y) = self.position
        right = self.right; left = self.left
        north = self.north; south = self.south
        east = self.east; west = self.west
        facing = self.facing

        if(facing % 2 == 0):
            for obs in warehouse.obstacles:
                if obs.x == x + 4:
                    
                    if obs.y == y + 13:
                        
                        self.turn(west)
                         
                        self.fwd(6, True)
                        
                        self.turn(north)
                        
                        self.fwd(25, True)
                         
                        self.turn(east)
                         
                        self.fwd(6, True)
                         
                        self.turn(north)
                        
                        return 25

                    elif obs.y == y-10:
                        
                        n = self.turn(west)
                        self.fwd(6, True)
                        self.turn(south)
                        self.fwd(25, True)
                        self.turn(east)
                        self.fwd(6, True)
                        self.turn(south)
                        return 25
                elif obs.x == x -7:

                    if obs.y == y + 13:
                        
                        n = self.turn(east)
                        
                        self.fwd(6, True)
                        
                        self.turn(north)
                        
                        self.fwd(25, True)
                        
                        self.turn(west)
                         
                        self.fwd(6, True)
                          
                        self.turn(north)
                        return 25

                        
                    elif obs.y == y-10:
                        
                        n = self.turn(east)
                        self.fwd(6, True)
                        self.turn(south)
                        self.fwd(25, True)
                        self.turn(west)
                        self.fwd(6, True)
                        self.turn(south)
                        return 25
            
        return 0
    def ping(self):
            (mX, mY) = self.position
            x =0; y =0
            pos = (x,y)
            x1 = 0
            y1 = 0
            x2 = 0
            y2 = 225
            x3 = 175
            y3 = 225
            r1 = sqrt(mX**2 + mY**2)
            r2 = sqrt(mX**2 + (mY-225)**2)
            r3 = sqrt((mX - 175)**2 + (mY-225)**2)
            x = round(-(y2 - y3)*((y2**2-y1**2)+(x2**2-x1**2)+(r1**2-r2**2)) + (y1-y2)*((y3**2-y2**2)+(x3**2-x2**2)+(r2**2-r3**2)))/(2*((x1-x2)*(y2-y3) - (x2-x3)*(y1-y2)))
            y = round(-(x2 - x3)*((x2**2 - x1**2) + (y2**2 - y1**2) + (r1**2 - r2**2))+((x1-x2)*((x3**2-x2**2)+(y3**2-y2**2)+(r2**2-r3**2))))/(2*((y1-y2)*(x2-x3) - (y2-y3)*(x1-x2)))
            pos = (x,y)
            print(pos)
            return pos

    def pickUpBox(self, box):
        facing = self.facing
        print("Pinging: ")
        
        print("picking up box")
        self.scan(box)
        

        if(box.barcode == self.desiredBarcode):
            self.ping()
            self.boxLocation = self.location
            self.box = box
            self.collectedBoxes[self.location[0]] += 1
            pyplot.pause(0.15)
            

            for _ in range(box.h):
                if not facing:
                    box.moveTimed((0, -1))

                elif facing == 2:
                    box.moveTimed((0, 1))
        else:
            box.x = 0
        pyplot.pause(0.15)

    

    def putDownBox(self):
        plot = self.plot
        box = self.box
        position = self.position
        (w, l) = self.size
        facing = self.facing

        print("putting down box")
        self.sprite = sprite = patches.Rectangle(position, l, w, linewidth = 1, edgecolor = 'black', facecolor = 'red')
        plot.add_patch(sprite)
        pyplot.pause(0.15)

        for _ in range(box.h):
            if not facing:
                box.moveTimed((0, 1))

            elif facing == 1:
                box.moveTimed((1, 0))

            elif facing == 2:
                box.moveTimed((0, -1))

            elif facing == 3:
                box.moveTimed((-1, 0))

        pyplot.pause(0.15)
        self.warehouse.boxes.remove(box)
        self.box.x = 0
        self.box = None
        self.sprite.remove()