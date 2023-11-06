import random
import sys
import math
from time import *
maxclustersize=0
class Vector2:
    def __init__(self, x, y):
        self.x=x
        self.y=y
    def __add__(self,vect2):
        return Vector2(self.x+vect2.x,self.y+vect2.y)
    def __sub__(self,vect2):
        return Vector2(self.x-vect2.x,self.y-vect2.y)
    def	__truediv__(self, divisor):
        if(divisor==0):
            answer=Vector2(0,0)
        else:
            answer=Vector2(self.x/divisor,self.y/divisor)
        return answer
    def __mul__(self, multiplicator):
        return Vector2(self.x*multiplicator,self.y*multiplicator)
    def __rmul__(self, multiplicator):
        return Vector2(self.x*multiplicator,self.y*multiplicator)
    def __NEG__(self):
        return Vector2(-self.x,-self.y)
    def __str__(self):
        return "x: "+str(self.x)+" y : "+str(self.y)
    
    
def VectorSquaredNorm(vector):
    return vector.x**2+vector.y**2

def VectorNormalized(vector):
    return vector/(VectorSquaredNorm(vector)**0.5)
def VectorScalarProd(vectorA,vectorB):
    return vectorA.x*vectorB.x+vectorA.y*vectorB.y

class Ball:
    def __init__(self, position, mass, radius, velocity):
        self.position=position
        self.mass = mass
        self.radius = radius
        self.velocity = velocity


def generateBallsSquareInGrid(grid,dimensions,numbOfBalls,SquareA,SquareB,mass,radius, velocity):
    """
    grid (list) a bidimensional list in which the Balls will be placed \n
    coeff (float 0-1) the probability coefficient ranging from 0 to 1 of a Ball being placed in a grid cell\n
    dimensions (Vector2) the dimensions of the plane in witch the balls can move (Vector2)\n
    mass (float) the mass of the balls
    velocity (Vector2) the velocity of the balls
    radius (float) the radius of the balls
    """
    balls=[]
    SquareDimensions=SquareB-SquareA
    coeff=math.sqrt(numbOfBalls/(SquareDimensions.x*SquareDimensions.y))
    for x in range(round(coeff*SquareDimensions.x)):
        for y in range(round(coeff*SquareDimensions.y)):
            newBall=Ball(Vector2(x/coeff+SquareA.x +SquareDimensions.x/(2*round(coeff*SquareDimensions.x)) ,y/coeff+SquareA.y+SquareDimensions.y/(2*round(coeff*SquareDimensions.y))), mass, radius, Vector2(velocity.x, velocity.y))
            balls.append(newBall)
            placeBallinGrid(newBall,grid,getGridDimensions(grid),dimensions)
    return balls

def addRandomSpeedsToBalls(balls,coeff):
    for aBall in balls:
        aBall.velocity+=Vector2(coeff*(random.random()-0.5)*2,coeff*(random.random()-0.5)*2)

def moveBallsInGrid(grid, deltaTime, dimensions, isCyclic, balls):
    """
    grid (list) the grid whose balls will be moved\n
    deltaTime (float) the time interval according to which the balls will be moved\n
    dimensions (Vector2) the dimensions of the plane in wich the balls can move (Vector2)\n
    isCyclic (Vect2(Bool)) whether or not the x,y dimensions are wrapped
    """
    gridDimensions=getGridDimensions(grid)
    grid=[[set() for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for aBall in balls:
        aBall.position+=aBall.velocity*deltaTime
        toCyclic(aBall.position, dimensions, isCyclic)
        placeBallinGrid(aBall, grid, gridDimensions, dimensions)
    return grid
def toCyclic(position,dimensions,isCyclic):
    if isCyclic.x:
        position.x=position.x%dimensions.x
    if isCyclic.y:
        position.y=position.y%dimensions.y
    
    
                

def getGridDimensions(grid):
    return Vector2(len(grid),len(grid[0]))
    
def placeBallinGrid(aBall, grid, gridDimensions, dimensions):
    """
    grid (list) the grid in which the ball will be placed\n
    gridDimensions (Vector2) the dimensions of the grid in wich the balls will be placed\n
    dimensions (Vector2) the dimensions of the plane in wich the balls can move (Vector2)\n(Vector2)
    """
    indexs=get2DGridIndexsFromPosition(gridDimensions,dimensions,aBall.position)
    grid[indexs[0]][indexs[1]].add(aBall)

def get2DGridIndexsFromPosition(gridDimensions,dimensions,position):
    return (get1DGridIndexFromPosition(gridDimensions.x,dimensions.x,position.x),get1DGridIndexFromPosition(gridDimensions.y,dimensions.y,position.y))

def get1DGridIndexFromPosition(gridDimension,dimension,position):
    """
    dimensions (Vector2) dimensions of the plane in wich the balls can move (Vector2)\n
    gridDimensions (Vector2) dimensions of the grid in wich the balls will be placed\n
    position (Vector2) position of the ball whose index in the grid we are searching\n
    /!\ doesn't apply cyclic properties of the grid /!\ 
    """
    returnIndex=0
    if( position==dimension ):
        returnIndex=gridDimension-1
    elif(position>dimension):
        returnIndex=gridDimension-1
    elif(position<0):
        pass
    else:
        returnIndex=round(position/dimension*gridDimension-0.5)
    return returnIndex

def applyCollisionsInGrid(grid, dimensions,isCyclic,balls):
    applyBoundsCollisions(grid,dimensions,isCyclic)

    
    gridDimensions=getGridDimensions(grid)
    for x in range(gridDimensions.x-1):
        for y in range(gridDimensions.y-1):
            applyCollisionsBetweenBallsSet(grid[x][y]|grid[x+1][y]|grid[x+1][y+1]|grid[x][y+1],dimensions,isCyclic,Vector2(False,False))
        y=gridDimensions.y-1
        if(isCyclic.y):
            applyCollisionsBetweenBallsSet(grid[x][y]|grid[x+1][y]|grid[x+1][0]|grid[x][0],dimensions,isCyclic,Vector2(False,False))
        else:
            applyCollisionsBetweenBallsSet(grid[x][y]|grid[x+1][y],dimensions,isCyclic,Vector2(False,False))

    x=gridDimensions.x-1
    if(isCyclic.x):
        for y in range(gridDimensions.y-1):
            applyCollisionsBetweenBallsSet(grid[x][y]|grid[0][y]|grid[0][y+1]|grid[x][y+1],dimensions,isCyclic,Vector2(True,False))
        if(isCyclic.y):
            applyCollisionsBetweenBallsSet(grid[x][gridDimensions.y-1]|grid[0][gridDimensions.y-1]|grid[0][0]|grid[x][0],dimensions,isCyclic,Vector2(True,True))
        else:
            applyCollisionsBetweenBallsSet(grid[x][gridDimensions.y-1]|grid[0][gridDimensions.y-1],dimensions,isCyclic,Vector2(True,True))

    else:
        for y in range(gridDimensions.y-1):
            applyCollisionsBetweenBallsSet(grid[x][y]|grid[x][y+1],dimensions,isCyclic,Vector2(True,False))
        y=gridDimensions.y-1
        if(isCyclic.y):
            applyCollisionsBetweenBallsSet(grid[x][y]|grid[x][0],dimensions,isCyclic,Vector2(True,True))
        else:
            applyCollisionsBetweenBallsSet(grid[x][y],dimensions,isCyclic,Vector2(True,True))
def applyCollisionsBetweenBallsSet(balls,dimensions,isCyclic, isBound):
    global maxclustersize
    #if(len(balls)>20): print(len(balls))
    if(len(balls)>maxclustersize):
        maxclustersize=len(balls)
        print("cluster size: ",maxclustersize)
    balls = list(balls)
    for index1 in range(len(balls)-1):
        for index2 in range(index1+1,len(balls)):
            #if(len(balls)>20): print(balls[index2].position.x,":",balls[index2].position.y)
            if(VectorSquaredNorm(balls[index1].position-balls[index2].position)**0.5<=balls[index1].radius+balls[index2].radius):
                collideBalls(balls[index1],balls[index2],dimensions,Vector2(False,False))

        if(isCyclic.x and isBound.x):
            for index1 in range(len(balls)-1):
                for index2 in range(index1+1,len(balls)):
                    #if(len(balls)>20): print(balls[index2].position.x,":",balls[index2].position.y)
                    xdistance=dimensions.x-abs(balls[index1].position.x-balls[index2].position.x)
                    ydistance=abs(balls[index1].position.y-balls[index2].position.y)
                    if((xdistance**2+ydistance**2)**0.5<=balls[index1].radius+balls[index2].radius):
                        collideBalls(balls[index1],balls[index2],dimensions,Vector2(True,False))
        if(isCyclic.y and isBound.y):
            for index1 in range(len(balls)-1):
                for index2 in range(index1+1,len(balls)):
                    #if(len(balls)>20): print(balls[index2].position.x,":",balls[index2].position.y)
                    xdistance=abs(balls[index1].position.x-balls[index2].position.x)
                    ydistance=dimensions.y- abs(balls[index1].position.y-balls[index2].position.y)
                    if((xdistance**2+ydistance**2)**0.5<=balls[index1].radius+balls[index2].radius):
                        collideBalls(balls[index1],balls[index2],dimensions,Vector2(False,True))
        if(isCyclic.y and isCyclic.x and isBound.x and isBound.y):
            for index1 in range(len(balls)-1):
                for index2 in range(index1+1,len(balls)):
                    #if(len(balls)>20): print(balls[index2].position.x,":",balls[index2].position.y)
                    xdistance=dimensions.x-abs(balls[index1].position.x-balls[index2].position.x)
                    ydistance=dimensions.y- abs(balls[index1].position.y-balls[index2].position.y)
                    if((xdistance**2+ydistance**2)**0.5<=balls[index1].radius+balls[index2].radius):
                        collideBalls(balls[index1],balls[index2],dimensions,Vector2(True,True))

def collideBalls(BallA,BallB, dimensions, isCyclicCollision):
    collision,VectAB,projVelA,projVelB =verifBallCollisionDirections(BallA.position,BallB.position,BallA.velocity,BallB.velocity,dimensions,isCyclicCollision)
    if (collision):


        newProjVelA=(projVelB*2*BallB.mass+projVelA*(BallA.mass-BallB.mass))/(BallA.mass+BallB.mass)
        newProjVelB=(projVelA*2*BallA.mass+projVelB*(BallB.mass-BallA.mass))/(BallA.mass+BallB.mass)


        BallA.velocity=BallA.velocity-(projVelA-newProjVelA)*VectAB
        BallB.velocity=BallB.velocity-(projVelB-newProjVelB)*VectAB
        
def sign(a):
    if(a<0):
        return -1
    return 1

def verifBallCollisionDirections(posA,posB,velA,velB, dimensions, isCyclicCollision):

    if(isCyclicCollision.x):
        xdistance=-sign(posB.x-posA.x)*(dimensions.x-abs(posB.x-posA.x))
    else:
        xdistance=posB.x-posA.x
    if(isCyclicCollision.y):
        ydistance=-sign(posB.y-posA.y)*(dimensions.y-abs(posB.y-posA.y))
    else:
        ydistance=posB.y-posA.y

    VectAB=Vector2(xdistance,ydistance)
    VectAB=VectorNormalized(VectAB)
    projVelA=VectorScalarProd(VectAB,velA)
    projVelB=VectorScalarProd(VectAB,velB)

    return (projVelA-projVelB>0,VectAB,projVelA,projVelB)

def applyBoundsCollisions(grid, dimensions, isCyclic):
    if(not isCyclic.y):
        for x in range(len(grid)):
            for aBall in grid[x][0]:
                if aBall.position.y<0:
                    aBall.position.y=-aBall.position.y
                    aBall.velocity.y=abs(aBall.velocity.y)
            for aBall in grid[x][len(grid[0])-1]:
                if aBall.position.y>dimensions.y:
                    aBall.position.y=dimensions.y-(aBall.position.y-dimensions.y)
                    aBall.velocity.y=-abs(aBall.velocity.y)
    if(not isCyclic.x):
        for y in range(len(grid[0])):
            for aBall in grid[0][y]:
                if aBall.position.x<0:
                    aBall.position.x=0
                    aBall.velocity.x=abs(aBall.velocity.x)
            for aBall in grid[len(grid)][y]:
                if aBall.position.x>dimensions.x:
                    aBall.position.x=dimensions.x
                    aBall.velocity.x=-abs(aBall.velocity.x)


def resetAndOpenDataFile(_path):
    
    storageData=open(_path,"w")
    storageData.write("")
    storageData.close()
    return open(_path,"a")

def appendBallsDataOnFile(_balls, _file):
    
    _file.write("!")
    for ball in _balls:
        _file.write("#p"+str(ball.position.x)+"x"+str(ball.position.y))
        _file.write("v"+str(ball.velocity.x)+"x"+str(ball.velocity.y))
        _file.write("m"+str(ball.mass))


def progress_bar(progression,starttime):
    remainingTime = round((1/(progression+0.0001)-1)* (time()-starttime),1)
    bar_length = 50  # number of characters in the progress bar
    progress = int(bar_length*progression)
    sys.stdout.write('\r')
    sys.stdout.write("[%-50s] %d%% remaining time :" % ('#' * progress, (100 * progression))+str(remainingTime))
    sys.stdout.flush()

def check_y_Velocity_Assymetry(Height,balls):
    smallesty=100
    biggesty=0
    topTot=0
    bottomTot=0
    ontheline=0
    yvel=0
    xvel=0
    for aBall in balls:
        if(aBall.position.y>Height/2):
            topTot+=VectorSquaredNorm( aBall.velocity)
        elif(aBall.position.y<Height/2):
            bottomTot+=VectorSquaredNorm( aBall.velocity)
        else:
            ontheline+=1
        yvel+=aBall.velocity.y
        xvel+=aBall.velocity.x
        if(smallesty>aBall.position.y):
            smallesty=aBall.position.y
        if(biggesty<aBall.position.y):
            biggesty=aBall.position.y
    print("top: ",topTot," bottom: ",bottomTot, " ontheline: ",ontheline, " yvelocity: ",yvel, " xvelocity: ",xvel," smallesty: ", smallesty, " biggesty: ", biggesty)

def checkBallsIndependency(balls):
    velocitiesandpositionsSet=set()
    ballsSet=set()
    for aBall in balls:
        if aBall.position in  velocitiesandpositionsSet:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
        velocitiesandpositionsSet.add(aBall.position)
        if aBall.velocity in  velocitiesandpositionsSet:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
        velocitiesandpositionsSet.add(aBall.velocity)
        if aBall in  ballsSet:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
        ballsSet.add(aBall)



        
