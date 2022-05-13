import tkinter as tk
from Counter import Counter
from Charger import Charger

from Dirt import Dirt
from Bot import Bot
from Astar import *
from Bin import Bin

def buttonClicked(x,y,registryActives):
    for rr in registryActives:
        if isinstance(rr,Bot):
            rr.x = x
            rr.y = y

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def register(canvas):
    # robot
    registryActives = []
    # wifi Hub,
    registryPassives = []
    noOfBots = 4
    noOfDirt = 300

    for i in range(0,noOfBots):
        bot = Bot("Bot"+str(i),canvas)
        registryActives.append(bot)
        bot.draw(canvas)
    charger = Charger("Charger")
    registryPassives.append(charger)
    charger.draw(canvas)
    bin = Bin("Bin",950,50)
    registryPassives.append(bin)
    bin.draw(canvas)
    #hub2 = WiFiHub("Hub1",50,500)
    #registryPassives.append(hub2)
    #hub2.draw(canvas)
    map = placeDirt(registryPassives, canvas)
    count = Counter(canvas)
    canvas.bind( "<Button-1>", lambda event: buttonClicked(event.x,event.y,registryActives) )
    return registryActives, registryPassives, count, map

def placeDirt(registryPassives,canvas):
    #places dirt in a specific configuration
    map = np.zeros( (10,10), dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                map[xx][yy] = random.randrange(1,3)
    i = 0
    for xx in range(10):
        for yy in range(10):
            for _ in range(map[xx][yy]):
                dirtX = xx*100 + random.randrange(0,99)
                dirtY = yy*100 + random.randrange(0,99)
                dirt = Dirt("Dirt"+str(i),dirtX,dirtY)
                registryPassives.append(dirt)
                dirt.draw(canvas)
                i += 1
    print(np.transpose(map))
    return map

def moveIt(canvas,registryActives,registryPassives,count,moves,map):
    moves += 1
    for rr in registryActives:
        #cal the dis to charger
        chargerIntensityL, chargerIntensityR = rr.senseCharger(registryPassives)
        binIntensityL, binIntensityR = rr.senseBin(registryPassives)

        rr.transferFunction(chargerIntensityL,chargerIntensityR,registryPassives,binIntensityL,binIntensityR,map)

        rr.move(canvas,registryPassives,1.0)

        registryPassives = rr.collectDirt(canvas,registryPassives, count)
       # numberOfMoves = 500
        #if moves>numberOfMoves:
           # print("total dirt collected in",numberOfMoves,"moves is",count.dirtCollected)
            #sys.exit()
    canvas.after(50,moveIt,canvas,registryActives,registryPassives,count,moves,map)

def main():
    window = tk.Tk()
    canvas = initialise(window)
    # robots and hub,wifi
    registryActives, registryPassives, count, map = register(canvas)
    moves = 0
    # Runs an endless loop
    # Adjusts the speed of the motors
    moveIt(canvas,registryActives,registryPassives, count, moves, map)
    window.mainloop()

main()
