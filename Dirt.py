import random

class Dirt:
    def __init__(self,namep,xx,yy):
        self.centreX = xx
        self.centreY = yy
        self.name = namep

    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-1,self.centreY-1, \
                                  self.centreX+1,self.centreY+1, \
                                  fill="grey",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY
