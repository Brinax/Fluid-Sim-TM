from time import *
import subprocess
WIDTH = 100
HEIGHT = 30

BALLS_RADIUS=5#0.26

GRIDWIDTH=int(WIDTH/(BALLS_RADIUS*2))
GRIDHEIGHT=int(HEIGHT/(BALLS_RADIUS*2))

from simulationLib import *

isCyclic = Vector2(True,False)
dimensions = Vector2(WIDTH,HEIGHT)

grid=[[set() for _ in range(int(GRIDHEIGHT))] for _ in range(GRIDWIDTH)]

#balls=generateBallsSquareInGrid(grid,dimensions,1,Vector2(0,0),Vector2(WIDTH,HEIGHT/2),1,BALLS_RADIUS,Vector2(0,0))
#balls+=generateBallsSquareInGrid(grid,dimensions,1,Vector2(0,HEIGHT/2),Vector2(WIDTH,HEIGHT),1,BALLS_RADIUS,Vector2(0,0))
newBall=Ball(Vector2(5,5), 1, 5, Vector2(0, 0.5))
balls=[newBall]
placeBallinGrid(newBall,grid,getGridDimensions(grid),dimensions)

addRandomSpeedsToBalls(balls,0.1)
print("numb of balls:",len(balls))

dataFile=resetAndOpenDataFile("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Simulations Particules Python/MySim0.3 Rayleigh/Data/data.txt")
numb_of_iterations=250000
deltaTime=0.002
starttime=time()
for index in range(numb_of_iterations):
    progress_bar(index/(numb_of_iterations-1),starttime)
    grid=moveBallsInGrid(grid,deltaTime,dimensions,isCyclic,balls)
    addGravitySpeedToBalls(balls,1,deltaTime)
    HeatandCoolGrid(grid,thickness=0.01,heatcoeff=5,coolcoeff=0)
    applyCollisionsInGrid(grid,dimensions,isCyclic,balls)
    if(index%500==0):
        appendBallsDataOnFile(balls,dataFile,dimensions)
#subprocess.call([r'C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/shutdown.bat'])
