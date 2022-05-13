import random
import math
import numpy as np
from Charger import Charger
from Dirt import Dirt
from Bin import Bin
from Astar import *

class Bot:

    def __init__(self,namep,canvasp):
        self.x = random.randint(100,900)
        self.y = random.randint(100,900)
        self.theta = random.uniform(0.0,2.0*math.pi)
        #self.theta = 0
        self.name = namep
        self.ll = 60 #axle width
        self.vl = 0.0
        self.r = 0.0
        self.battery = 1000
        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.map = np.zeros( (10,10) )
        self.canvas = canvasp
        self.dirtCollected = 0

    # draw the canvas
    def draw(self,canvas):
        points = [ (self.x + 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x + 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                ]
        # draw the robot
        canvas.create_polygon(points, fill="blue", tags=self.name)
        # sensor position
        self.sensorPositions = [ (self.x + 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y - 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                                 (self.x - 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y + 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                            ]
    
        centre1PosX = self.x 
        centre1PosY = self.y
        # create the robot yellow oval with number in it
        canvas.create_oval(centre1PosX-15,centre1PosY-15,\
                           centre1PosX+15,centre1PosY+15,\
                           fill="gold",tags=self.name)
        # create the battery dirt count
        canvas.create_text(self.x,self.y,text=str(self.battery),tags=self.name)
        canvas.create_text(self.x + 30,self.y + 30,text=str(self.dirtCollected),tags=self.name)

        wheel1PosX = self.x - 30*math.sin(self.theta)
        wheel1PosY = self.y + 30*math.cos(self.theta)
        canvas.create_oval(wheel1PosX-3,wheel1PosY-3,\
                                         wheel1PosX+3,wheel1PosY+3,\
                                         fill="red",tags=self.name)

        wheel2PosX = self.x + 30*math.sin(self.theta)
        wheel2PosY = self.y - 30*math.cos(self.theta)
        canvas.create_oval(wheel2PosX-3,wheel2PosY-3,\
                                         wheel2PosX+3,wheel2PosY+3,\
                                         fill="green",tags=self.name)

        # positions for sensors sensor1(sensorPositions[0],sensorPositions[1])
        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        canvas.create_oval(sensor1PosX-3,sensor1PosY-3, \
                           sensor1PosX+3,sensor1PosY+3, \
                           fill="yellow",tags=self.name)
        canvas.create_oval(sensor2PosX-3,sensor2PosY-3, \
                           sensor2PosX+3,sensor2PosY+3, \
                           fill="yellow",tags=self.name)
        
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self,canvas,registryPassives,dt):
        #deduce battery every move
        if self.battery>0:
            self.battery -= 1

        if self.battery==0:
            self.vl = 0
            self.vr = 0
        # while robot is within 10 of the charger the battery will add
        for rr in registryPassives:
            if isinstance(rr,Charger) and self.distanceTo(rr)<80:
                self.battery += 10

            if isinstance(rr,Bin) and self.distanceTo(rr)<80:
                self.dirtCollected = 0
                
        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))
        omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) #instantaneous centre of curvature
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(omega*dt), -math.sin(omega*dt), 0], \
                        [math.sin(omega*dt), math.cos(omega*dt), 0],  \
                        [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[omega*dt]])
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta%(2.0*math.pi) #make sure angle doesn't go outside [0.0,2*pi)
        self.x = newX
        self.y = newY
        self.theta = newTheta        
        if self.vl==self.vr: # straight line movement
            self.x += self.vr*math.cos(self.theta) #vr wlog
            self.y += self.vr*math.sin(self.theta)
        if self.x<0.0:
            self.x=999.0
        if self.x>1000.0:
            self.x = 0.0
        if self.y<0.0:
            self.y=999.0
        if self.y>1000.0:
            self.y = 0.0
        self.updateMap()
        canvas.delete(self.name)
        self.draw(canvas)

    def updateMap(self):
        xMapPosition = int(math.floor(self.x/100))
        yMapPosition = int(math.floor(self.y/100))
        self.map[xMapPosition][yMapPosition] = 1
        self.drawMap()

    def drawMap(self):
        for xx in range(0,10):
            for yy in range(0,10):
                print(xx,",",yy,)
                # if self.map[xx][yy]==1:
                    # self.canvas.create_rectangle(100*xx,100*yy,100*xx+100,100*yy+100,fill="pink",width=0,tags="map")
        self.canvas.tag_lower("map")
                
    # cal the distance to charger
    def senseCharger(self, registryPassives):
        lightL = 0.0
        lightR = 0.0
        for pp in registryPassives:
            # if pp is charger
            if isinstance(pp,Charger):
                lx,ly = pp.getLocation()
                # distance to sensor1
                distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                                       (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                # distance to sensor2
                distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                                       (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )

                lightL += 200000/(distanceL*distanceL)
                lightR += 200000/(distanceR*distanceR)
        return lightL, lightR

    def senseBin(self, registryPassives):
        lightL = 0.0
        lightR = 0.0
        for pp in registryPassives:
            # if pp is charger
            if isinstance(pp,Bin):
                lx,ly = pp.getLocation()
                # distance to sensor1
                distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                                       (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                # distance to sensor2
                distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                                       (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )

                lightL += 200000/(distanceL*distanceL)
                lightR += 200000/(distanceR*distanceR)
        return lightL, lightR

    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )

    def collectDirt(self, canvas, registryPassives, count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr,Dirt):
                # within the distance of 30 will be collected
                if self.distanceTo(rr)<30:
                    self.dirtCollected += 1
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives

    # chargerL and chargerR refers to the distance to Charger.
    def transferFunction(self,chargerL,chargerR,registryPassives,binL,binR,map):
        # wandering behaviour
        # when the vl set to <0 the left wheel wouldn't move
        if self.currentlyTurning==True:
            self.vl = -2.0
            self.vr = 2.0
            self.turning -= 1
        else:
            self.vl = 5.0
            self.vr = 5.0
            self.moving -= 1
        # if not moving and not turing change the the turing to true
        if self.moving==0 and not self.currentlyTurning:
            self.turning = random.randrange(20,40)
            self.currentlyTurning = True
        # if not turing, move
        if self.turning==0 and self.currentlyTurning:
            self.moving = random.randrange(50,100)
            self.currentlyTurning = False
        # battery - these are later so they have priority
        if self.battery<600:
            # find the best path to the charger
            charger = registryPassives[0]
            path, cost = a_star_search(map, (math.floor(self.x/100), math.floor(self.y/100)), (math.floor(charger.centreX/100),math.floor(charger.centreY/100)))
            print("best route to charger： " , path)
            print("cost to charger： " , cost)
            if(self.dirtCollected >= 10):
                bin = registryPassives[1]
                if((math.floor(bin.centreX/100),math.floor(bin.centreY/100) in path)):
                    # 设置使机器人先访问垃圾桶
                    print("visit bin")
            else:
                print("visit charger")
            if chargerR>chargerL:
                self.vl = 2.0
                self.vr = -2.0
            elif chargerR<chargerL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(chargerR-chargerL)<chargerL*0.1: #approximately the same
                self.vl = 5.0
                self.vr = 5.0
            #self.vl = 5*math.sqrt(chargerR)
            #self.vr = 5*math.sqrt(chargerL)
        if self.dirtCollected > 20:
            # find the best path to the charger
            bin = registryPassives[1]
            path, cost = a_star_search(map, (math.floor(self.x / 100), math.floor(self.y / 100)),
                                       (math.floor(bin.centreX / 100), math.floor(bin.centreY / 100)))
            print("best route to bin： ", path)
            print("cost to bin： ", cost)
            if (self.dirtCollected >= 10):
                bin = registryPassives[1]
                if ((math.floor(bin.centreX / 100), math.floor(bin.centreY / 100) in path)):
                    # 设置使机器人先访问垃圾桶
                    print("visit bin")
            if binR>binL:
                self.vl = 2.0
                self.vr = -2.0
            elif binR<binL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(binR-binL)<binL*0.1: #approximately the same
                self.vl = 5.0
                self.vr = 5.0
            #self.vl = 5*math.sqrt(chargerR)
            #self.vr = 5*math.sqrt(chargerL)
        if chargerL+chargerR>200 and self.battery<1000:
            self.vl = 0.0
            self.vr = 0.0


