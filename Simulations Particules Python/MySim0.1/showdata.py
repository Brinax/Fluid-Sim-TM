from tkinter import *     
from PIL import Image,ImageTk
from time import *

root = Tk()
canvas = Canvas(root, width = 2000, height = 1080)      
canvas.pack()  
ballImg=Image.open("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Simulations Particules Python/MySim0.1/circle.png")
fixedTimeStep=0.02
dataPath="C:/Users/lcach/Documents/4-Ecole/Physique/TM/Simulations Particules Python/MySim0.3 Rayleigh/Data/data.txt"

class Vector2:
    def __init__(self,theX,theY):
        self.x=theX
        self.y=theY
    def __mul__(self,factor):
        return Vector2(self.x*factor,self.y*factor)

class BallImg:
    def __init__(self,thePosition):
        self.position=thePosition
        self.radius=5
        self.theImg = ImageTk.PhotoImage(ballImg.resize((self.radius*5,self.radius*5), Image.ANTIALIAS))
        self.img=canvas.create_image(thePosition.x,thePosition.y, anchor=CENTER, image=self.theImg)
    def updatePos(self,newPosition):
        self.position=newPosition
        canvas.coords(self.img,self.position.x-self.radius,self.position.y-self.radius) 
class Ball:
    def __init__(self,thePosition):
        self.position=thePosition

def unpackData(dataPath):
    datatxt=open(dataPath,"r").read()
    FramesData=datatxt[1:].split("!")
    for (frameIndex,frameData) in enumerate(FramesData):
        FramesData[frameIndex]=frameData[1:].split("#")#[4400:5200]
        for (ballIndex,ballData) in enumerate(FramesData[frameIndex]):
            posData=ballData[ballData.index("p")+1:ballData.index("v")]
            posData=posData.split("x")
            FramesData[frameIndex][ballIndex]=Ball(Vector2(float(posData[0]),float(posData[1])))
    return FramesData

simulationData=unpackData(dataPath)
Balls=[]
for (index,aBall) in enumerate(simulationData[0]):
    Balls.append(BallImg(simulationData[0][index].position))

frameIndex=0
thetime=time()
while frameIndex<len(simulationData):
    
    timedelay=(time()-thetime)
    while timedelay<fixedTimeStep:
        timedelay=(time()-thetime)
    thetime=time()
    #print(timedelay)

    for (index,ball) in enumerate(Balls):
        ball.updatePos(simulationData[frameIndex][index].position*10)

    canvas.configure(bg="grey")
    root.update_idletasks()
    root.update()
    frameIndex+=1