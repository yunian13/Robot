class Counter:
    def __init__(self,canvas):
        self.dirtCollected = 0
        self.canvas = canvas
        self.canvas.create_text(70,50,text="Dirt collected: "+str(self.dirtCollected),tags="counter")

    # item collected
    def itemCollected(self, canvas):
        self.dirtCollected +=1
        self.canvas.itemconfigure("counter",text="Dirt collected: "+str(self.dirtCollected))