from tkinter import *  
import time
import math as math
from tkinter import constants    
from PIL import Image,ImageTk
import random

Balls=[]
xLimit=1000
yLimit=500
numbOfBallsToGen=100
fps=60


class Vector2:
    def __init__(self,theX,theY):
        self.x=theX
        self.y=theY
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
    def __NEG__(self, OTHER):
        return Vector2(-self.x,-self.y)
    def magnitude(self):
        return (self.x**2+self.y**2)**(1/2)
    def mult(self,nb):
        return Vector2(self.x*nb,self.y*nb)
    def normalized(self):
        return self/self.magnitude()
    def radAngle(self):
        return math.acos(self.normalized().x)


class Ball:
    def __init__(self,theVelocity,thePosition,theRadius,theMass):
        self.Velocity=theVelocity
        self.Position=thePosition
        self.radius=theRadius
        self.mass=theMass
        self.theImg = ImageTk.PhotoImage(ballImg.resize((theRadius*2,theRadius*2), Image.ANTIALIAS))
        self.img=canvas.create_image(thePosition.x,thePosition.y, anchor=NW, image=self.theImg) 
        self.collidingBalls= set()

    def MoveBySpeed(self,time):
        self.Position+=self.Velocity.mult(time)
        if(self.Position.x>xLimit or self.Position.x<0):
            self.Velocity.x*=-1
            if self.Position.x<0:
                self.Position.x=0
            else:
                self.Position.x=xLimit
        if(self.Position.y>yLimit or self.Position.y<0):
            self.Velocity.y*=-1
            if self.Position.y<0:
                self.Position.y=0
            else:
                self.Position.y=yLimit
        #print(str(self.Velocity.y)+" : "+str(self.Position.y))
        canvas.coords(self.img,self.Position.x-self.radius,self.Position.y-self.radius) 

    def Collide(self,Ball2):
        initKinE=(self.Velocity.x**2+self.Velocity.y**2)*self.mass+(Ball2.Velocity.x**2+Ball2.Velocity.y**2)*Ball2.mass
        #print(initKinE)
        CollisionVector1 = Ball2.Position - self.Position
        angle1 = AngleBetweenVectors(CollisionVector1,self.Velocity)
        #print(str(angle1)+" : "+str(AngleBetweenVectors(CollisionVector1,self.Velocity)))
        directCollisionVector1 = CollisionVector1.normalized() *math.cos(angle1) * self.Velocity.magnitude()
        savedSpeed1 = self.Velocity - directCollisionVector1
        xCollisionSpeed1 = directCollisionVector1.x
        yCollisionSpeed1 = directCollisionVector1.y



        CollisionVector2 = CollisionVector1*-1
        SpeedVector2 = Ball2.Velocity
        angle2 = AngleBetweenVectors(CollisionVector2,SpeedVector2)
        directCollisionVector2 = CollisionVector2.normalized() * math.cos(angle2) * SpeedVector2.magnitude()
        savedSpeed2=Ball2.Velocity - directCollisionVector2
        xCollisionSpeed2 = directCollisionVector2.x
        yCollisionSpeed2 = directCollisionVector2.y


        self.Velocity.x = (2 * Ball2.mass * xCollisionSpeed2 + (self.mass - Ball2.mass) * xCollisionSpeed1) / (self.mass + Ball2.mass) + savedSpeed1.x
        self.Velocity.y = (2 * Ball2.mass * yCollisionSpeed2 + (self.mass - Ball2.mass) * yCollisionSpeed1) / (self.mass + Ball2.mass) + savedSpeed1.y
        Ball2.Velocity.x = (2 * self.mass * xCollisionSpeed1 + (Ball2.mass - self.mass) * xCollisionSpeed2) / (self.mass + Ball2.mass) + savedSpeed2.x
        Ball2.Velocity.y = (2 * self.mass * yCollisionSpeed1 + (Ball2.mass - self.mass) * yCollisionSpeed2) / (self.mass + Ball2.mass) + savedSpeed2.y
        finKinE=(self.Velocity.x**2+self.Velocity.y**2)*self.mass+(Ball2.Velocity.x**2+Ball2.Velocity.y**2)*Ball2.mass
        #print(finKinE)
        if(finKinE-initKinE>1):
            print('rien ne se crée, rien ne se perd, tout de transforme! mais pas la =(')

def scalProd(vect1,vect2):
    return vect1.x*vect2.x+vect1.y*vect2.y
def AngleBetweenVectors(Vect1,Vect2):
    if((Vect1.magnitude()*Vect2.magnitude())==0):
        answer=0
    else:
        answer=math.acos(scalProd(Vect1,Vect2)/(Vect1.magnitude()*Vect2.magnitude()))
    return answer
def UpdateBallPositions(time):
    for i in range(len(Balls)):
        Balls[i].MoveBySpeed(time)

def checkBallCollisions():
    for i1 in range(len(Balls)):
        for i2 in range(i1+1,len(Balls)):
            BallsPosDiff=Balls[i1].Position-Balls[i2].Position
            RadiusSumm=Balls[i1].radius+Balls[i2].radius
            if(abs(BallsPosDiff.x)>RadiusSumm or abs(BallsPosDiff.y)>RadiusSumm or BallsPosDiff.x**2+BallsPosDiff.y**2>RadiusSumm**2):
                Balls[i1].collidingBalls.discard(i2)
            elif(i2 not in Balls[i1].collidingBalls):
                Balls[i1].collidingBalls.add(i2)
                Balls[i1].Collide(Balls[i2])
def generateBalls():
    for i in range(numbOfBallsToGen):
        Balls.append(Ball(Vector2(random.random()*200-100,random.random()*200-100),Vector2(random.random()*xLimit,random.random()*yLimit),round(random.random()*5+5),random.random()*4+1))

            



root = Tk()
canvas = Canvas(root, width = 2000, height = 1080)      
canvas.pack()  
ballImg=Image.open("C:/Users/lcach/Documents/2-Programmation/python/MovingBalls/myMovingBallsV0_0/circle.png")
generateBalls()
"""Balls.append(Ball(Vector2(-200,-60),Vector2(200,330),100,10))
Balls.append(Ball(Vector2(200,0),Vector2(0,170),50,5))
Balls.append(Ball(Vector2(200,0),Vector2(0,180),50,10))
Balls.append(Ball(Vector2(200,0),Vector2(0,190),50,10))"""
thetime=time.time()
while True:
    actualTime=time.time()
    timedelay=(actualTime-thetime)
    if(timedelay!=0):
        fps=(fps*59+(1/timedelay))/60
        #print(fps)
        root.title(fps)
    
    #print(str(timedelay)+" : "+str(actualTime)+" : "+str(thetime))
    checkBallCollisions()
    UpdateBallPositions(0.02)
    canvas.configure(bg="grey")
    root.update_idletasks()
    root.update()
    thetime=actualTime
    #print(actualTime)
