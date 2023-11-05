import math
import numpy
class Vector2:
    x=0
    y=0
    def __init__(self,x,y) -> None:
        self.x=x
        self.y=y
    def floor(self):
        x=math.floor(self.x)
        y=math.floor(self.y)
        return Vector2(x,y)
    def frac(self):
        x=self.x-math.floor(self.x)
        y=self.y-math.floor(self.y)
        return Vector2(x,y)
    def __add__(self,vector):
        x=self.x+vector.x
        y=self.y+vector.y
        return Vector2(x,y)
    def __sub__(self,vector):
        x=self.x-vector.x
        y=self.y-vector.y
        return Vector2(x,y)
    def __mul__(self,other):
        if(type(other)==Vector2):
            return self.x*other.x+self.y*other.y
        x=self.x*other
        y=self.y*other
        return Vector2(x,y)
    def __rmul__(self,other):
        if(type(other)==Vector2):
            return self.x*other.x+self.y*other.y
        x=self.x*other
        y=self.y*other
        return Vector2(x,y)
    def __truediv__(self,other):
        if(type(other)==Vector2):
            if(other.module()==0):
                if(self.module()==0):
                    return 0
                else:
                    print("impossible div!")
                    return None
            if(other.x!=0):
                coeff=self.x/other.x
            else:
                coeff=self.y/other.y
            if((other.y==0 and self.y!=0) or (other.y!=0 and abs(self.y/other.y-coeff)>0.001)):
                print("impossible to divide vectors! ",self,other)
            else:
                return coeff
        x=self.x/other
        y=self.y/other
        return Vector2(x,y)
    def __round__(self):
        x=round(self.x)
        y=round(self.y)
        return Vector2(x,y)
    def __str__(self):
        return str(self.x)+":"+str(self.y)
    def module(self):
        return math.sqrt(self.x**2+self.y**2)
    def unit(self):
        if(self.module()==0):
            return self
        return self/self.module()

def absAngleBetweenVects(VectA,VectB):
    product=VectA.unit()*VectB.unit()
    if(abs(product)>1):
        product/=abs(product)
    return math.acos(product)

def angleBetweenVects(VectA,VectB):
    if(VectA.module()==0 or VectB.module()==0):
        return 0
    projectionOf_B_on_A=VectA*VectB*VectA/(VectB.module()*VectA.module()**2)
    rest=VectB/VectB.module()-projectionOf_B_on_A
    if(VectA.x!=0):
        return math.acos(round(projectionOf_B_on_A.module(),5))*numpy.sign(rest.y/-VectA.x)
    else:
        return math.acos(round(projectionOf_B_on_A.module(),5))*numpy.sign(rest.x/VectA.y)

def getDataSetIndexesInDataFile(filePath):
    global width,height
    indexes=[]
    f=open(filePath,"r")
    filetext=f.read()
    if(len(filetext.split("W"))>1):
        filetext=filetext.split("W")
        width=int(filetext[0])
        height=width
        lenToAdd=len(filetext[0])
        filetext=filetext[1]
        indexes.append(lenToAdd+1)
    for i,c in enumerate(filetext):
        if(c=="#"):
            indexes.append(i+lenToAdd+2)
    return indexes

def readDataInInterval(filePath,startIndex,endIndex):
    f=open(filePath,"r")
    filetext=f.read()
    dataSet=filetext[startIndex:endIndex]
    return [float(data) for data in dataSet.split("\\")[0:-1]]

def lerp(a,b,k):
    return a+k*(b-a)
def GetVel(x,y):
    if(y<0 or y>=height):
        return boundsVelocity
    return velocities[posToIndex(Vector2(x,y))]
def getCurl(pos):
    if(isAlongVel):
        referenceAnglePos=pos-velocities[posToIndex(pos)]
    else:
        referenceAnglePos=pos-velocities[posToIndex(pos)].unit()
    i=referenceAnglePos.floor()
    j=referenceAnglePos.frac()
    z1=lerp(GetVel(y=i.y,x=i.x).x,GetVel(y=i.y,x=i.x+1).x,j.x)
    z2=lerp(GetVel(y=i.y+1,x=i.x).x,GetVel(y=i.y+1,x=i.x+1).x,j.x)
    refxVel=lerp(z1,z2,j.y)
    z1=lerp(GetVel(y=i.y,x=i.x).y,GetVel(y=i.y,x=i.x+1).y,j.x)
    z2=lerp(GetVel(y=i.y+1,x=i.x).y,GetVel(y=i.y+1,x=i.x+1).y,j.x)
    refyVel=lerp(z1,z2,j.y)
    return angleBetweenVects(Vector2(refxVel,refyVel),velocities[posToIndex(pos)])

def getCurlField():
    curlField=[None]*width*height
    for y in range(height):
        for x in range(width):
            curlField[posToIndex(Vector2(x,y))]=getCurl(Vector2(x,y))
    return curlField

def posToIndex(vector):
    if(isCylinder):
        return vector.y*width+(vector.x%width)
    return vector.y*width+vector.x

def resetFileAndOpen(dirTxT):
    f = open(dirTxT, "w")
    f.write(str(width)+"W")
    f.close()
    return open(dirTxT,"a")
def dataToString(dataArray):
    txt=""
    for data in dataArray:
        rounded=round(data,2)
        txt+=str(rounded)+"\\"
    return txt
isAlongVel=False
isCylinder=True
width=30
height=30
boundsVelocity=Vector2(0,0)

velXDataSetIndexes=getDataSetIndexesInDataFile("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityXdata.txt")
velYDataSetIndexes=getDataSetIndexesInDataFile("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityYdata.txt")
frameIndex=0

curlF = resetFileAndOpen("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/curlData.txt")

while frameIndex<len(velXDataSetIndexes)-1:
    velocityX=readDataInInterval("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityXdata.txt",velXDataSetIndexes[frameIndex],velXDataSetIndexes[frameIndex+1])
    velocityY=readDataInInterval("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityYdata.txt",velYDataSetIndexes[frameIndex],velYDataSetIndexes[frameIndex+1])
    velocities=[]
    for (index,data) in enumerate(velocityX):
        velocities.append(Vector2(velocityX[index],velocityY[index]))

    curlF.write(dataToString(getCurlField())+"#")

    
    if frameIndex%10==0:
        print(round(frameIndex/(len(velXDataSetIndexes)-1)*100,1),"%")
    frameIndex+=1