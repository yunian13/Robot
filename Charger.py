import random

class Charger:
    def __init__(self, namep):
        self.centreX = random.randint(100, 900)
        self.centreY = random.randint(100, 900)
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 10, self.centreY - 10, \
                                  self.centreX + 10, self.centreY + 10, \
                                  fill="gold", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY
