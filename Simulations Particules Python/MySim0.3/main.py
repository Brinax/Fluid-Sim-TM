from time import *
import subprocess
WIDTH = 100
HEIGHT = 30

BALLS_RADIUS=0.25

GRIDWIDTH=int(WIDTH/(BALLS_RADIUS*2))
GRIDHEIGHT=int(HEIGHT/(BALLS_RADIUS*2))

from simulationLib import *

isCyclic = Vector2(True,False)
dimensions = Vector2(WIDTH,HEIGHT)

grid=[[set() for _ in range(int(GRIDHEIGHT))] for _ in range(GRIDWIDTH)]

balls=generateBallsSquareInGrid(grid,dimensions,3612,Vector2(0,0),Vector2(WIDTH,HEIGHT/2),1,BALLS_RADIUS,Vector2(4.5,0))
balls+=generateBallsSquareInGrid(grid,dimensions,3612,Vector2(0,HEIGHT/2),Vector2(WIDTH,HEIGHT),1,BALLS_RADIUS,Vector2(-4.5,0))


addRandomSpeedsToBalls(balls,0.5)
print("numb of balls:",len(balls))

dataFile=resetAndOpenDataFile("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Simulations Particules Python/MySim0.3/Data/data.txt")
numb_of_iterations=100000
starttime=time()
for index in range(numb_of_iterations):
    progress_bar(index/(numb_of_iterations-1),starttime)
    grid=moveBallsInGrid(grid,0.001,dimensions,isCyclic,balls)
    applyCollisionsInGrid(grid,dimensions,isCyclic,balls)
    if(index%200==0):
        appendBallsDataOnFile(balls,dataFile)
#subprocess.call([r'C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/shutdown.bat'])

