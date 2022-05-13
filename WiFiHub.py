class WiFiHub:
    def __init__(self, namep, xp, yp):
        self.centreX = xp
        self.centreY = yp
        self.name = namep

    def draw(self, canvas):
        body = canvas.create_oval(self.centreX - 10, self.centreY - 10, \
                                  self.centreX + 10, self.centreY + 10, \
                                  fill="purple", tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY
