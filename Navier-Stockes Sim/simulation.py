import math
import random
import time
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
    def __mul__(self,const):
        x=self.x*const
        y=self.y*const
        return Vector2(x,y)
    def __truediv__(self,const):
        x=self.x/const
        y=self.y/const
        return Vector2(x,y)
    def __round__(self):
        x=round(self.x)
        y=round(self.y)
        return Vector2(x,y)
    def __str__(self):
        return str(self.x)+":"+str(self.y)
    def module(self):
        return math.sqrt(self.x**2+self.y**2)

width=50
height=50
densities=[0]*width*height
velocities=[]
AdjacentVectors=[Vector2(1,0),Vector2(-1,0),Vector2(0,-1),Vector2(0,1)]
for _ in range(width*height):
    velocities.append(Vector2(0,0))
boundsDensitie=0
boundsVelocities=[]
for _ in range(2*width+2*height):
    boundsVelocities.append(Vector2(0,0))
densityDiffusion=0
velocityDiffusion=0.01
velocityDiffusionAcuracy=20
diffusionAcuracy=20
divergenceAcuracy=50

isReset=False
isDensityOnly=True
isCylinder=True

def createAWall(array,pos1,pos2,value,indexFunc=lambda vector:vectToIndexRounded(vector)):
    pos1=pos1.floor()
    pos2=pos2.floor()
    if((pos2-pos1).module()%1==0):
        for i in range(round((pos2-pos1).module()+1)):
            PosToFill=pos1+(pos2-pos1)*(1/(pos2-pos1).module())*i
            array[indexFunc(PosToFill)]=value
    return array
def createAWallByFunc(array,pos1,pos2,valueFunc,indexFunc=lambda vector:vectToIndexRounded(vector)):
    pos1=pos1.floor()
    pos2=pos2.floor()
    if((pos2-pos1).module()%1==0):
        for i in range(round((pos2-pos1).module()+1)):
            PosToFill=pos1+(pos2-pos1)*(1/(pos2-pos1).module())*i
            array[indexFunc(PosToFill)]=valueFunc()
    return array
def createARectangle(array,pos1,pos2,value):
    pos1=pos1.floor()
    pos2=pos2.floor()
    rectangleVector=pos2-pos1
    for x in range(abs(rectangleVector.x)+1):
        array=createAWall(array,pos1+Vector2(x,0),pos1+Vector2(x,rectangleVector.y),value)
    return array

def createARectangleByFunc(array,pos1,pos2,valueFunc):
    pos1=pos1.floor()
    pos2=pos2.floor()
    rectangleVector=pos2-pos1
    for x in range(abs(rectangleVector.x)+1):
        array=createAWallByFunc(array,pos1+Vector2(x,0),pos1+Vector2(x,rectangleVector.y),valueFunc)
    return array



def isOutOfSim(Vector):
    x=Vector.x
    y=Vector.y
    if(y<0 or y>=height):
        return True
    if(not isCylinder and(x<0 or x>=width) ):
        return True
    return False
def PrintDensities():
    text=""
    for y in range(height):
        for x in range(width):
            if(densities[posToIndex(x,y)]>0.5):
                posTxt="1"
            else:posTxt="0"
            text+=" "+posTxt
        text+="\n"
    print(text)
def PrintVelocities():
    text=""
    for y in range(height):
        for x in range(width):
            posTxt=str(round(velocities[posToIndex(x,y)].module()))
            text+=" "+posTxt
        text+="\n"
    print(text)

def GetDensity(x,y):
    if(y<0 or y>=height):
        return boundsDensitie
    if(x<0 or x>=width):
        if(isCylinder):
            x=x%width
        else:
            return boundsDensitie
    
    return densities[y*width+x]

def GetVelocity(x,y):
    if(y<0 or y>=height):
        return boundsVelocities[boundVectToIndex(Vector2(x,y))]
    if(x<0 or x>=width):
        if(isCylinder):
            x=x%width
        else:
            return boundsVelocities[boundVectToIndex(Vector2(x,y))]
    return velocities[y*width+x]


def DensityDiffusion():
    global densities
    EqArray=[None]*width*height
    varsEqArray=[[None,None,None,None] for _ in range(height*width)]

    for y in range(height):
        for x in range(width):
            varsFactor=densityDiffusion/((1+densityDiffusion*4))#modified from video
            EqArray[posToIndex(x,y)]=[varsFactor,varsFactor,varsFactor,varsFactor,densities[posToIndex(x,y)]/(1+densityDiffusion*4)]#modified from video
            for (index,vector) in enumerate(AdjacentVectors):
                resultV=Vector2(x,y)+vector
                if(isOutOfSim(resultV)):
                    EqArray[posToIndex(x,y)][index]*=boundsDensitie
                else:
                    varsEqArray[posToIndex(x,y)][index]=vectToIndex(resultV)
    densities = GaussSeidel(width*height,EqArray,varsEqArray,diffusionAcuracy)
def VelocityDiffusion():
    global velocities
    #matriceToSolve=[0]*((height*width)**2)
    EqArrayx=[None]*width*height
    varsEqArrayx=[[None,None,None,None] for _ in range(height*width)]
    EqArrayy=[None]*width*height
    varsEqArrayy=[[None,None,None,None] for _ in range(height*width)]

    for y in range(height):
        for x in range(width):
            varsFactor=velocityDiffusion/((1+velocityDiffusion*4))#modified from video
            EqArrayx[posToIndex(x,y)]=[varsFactor,varsFactor,varsFactor,varsFactor,velocities[posToIndex(x,y)].x/(1+4*velocityDiffusion)]#modified from video
            EqArrayy[posToIndex(x,y)]=[varsFactor,varsFactor,varsFactor,varsFactor,velocities[posToIndex(x,y)].y/(1+4*velocityDiffusion)]#modified from video
            for (index,vector) in enumerate(AdjacentVectors):
                resultV=Vector2(x,y)+vector
                if(isOutOfSim(resultV)):
                    EqArrayx[posToIndex(x,y)][index]*=boundsVelocities[boundVectToIndex(resultV)].x
                    EqArrayy[posToIndex(x,y)][index]*=boundsVelocities[boundVectToIndex(resultV)].y
                else:
                    varsEqArrayx[posToIndex(x,y)][index]=vectToIndex(resultV)
                    varsEqArrayy[posToIndex(x,y)][index]=vectToIndex(resultV)

    velocitiesx = GaussSeidel(width*height,EqArrayx,varsEqArrayx,velocityDiffusionAcuracy)
    velocitiesy = GaussSeidel(width*height,EqArrayy,varsEqArrayy,velocityDiffusionAcuracy)
    for i in range(len(velocities)):
        velocities[i]=Vector2(velocitiesx[i],velocitiesy[i])

#in Eq arrays la dérnière valeur de chaque chaîne doit être la constante dans l'équation
def GaussSeidel(numbOfVars,EqArrays,varsEqArrays,numbOfIterations):
    solvedVariables=[0]*numbOfVars
    #newsolvedVariables=[0]*numbOfVars GaussSeidel not jacobi!
    for _ in range(numbOfIterations):
        for i in range(numbOfVars):
            varAnsw=EqArrays[i][-1]
            for i2 in range(len(EqArrays[i])-1):
                if(varsEqArrays[i][i2]==None):
                    varAnsw+=EqArrays[i][i2]
                else:
                    varAnsw+=solvedVariables[varsEqArrays[i][i2]]*EqArrays[i][i2]
            solvedVariables[i]=varAnsw
    return solvedVariables

def lerp(a,b,k):
    return a+k*(b-a)

def DensityAdvection(deltaTime):
    global densities
    new_densities=[None]*width*height
    for y in range(height):
        for x in range(width):
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            f=Vector2(x,y)-velocities[posToIndex(x,y)]*deltaTime
            i=f.floor()
            j=f.frac()
            z1=lerp(GetDensity(y=i.y,x=i.x),GetDensity(y=i.y,x=i.x+1),j.x)
            z2=lerp(GetDensity(y=i.y+1,x=i.x),GetDensity(y=i.y+1,x=round(i.x)+1),j.x)
            new_densities[posToIndex(x,y)]=lerp(z1,z2,j.y)
    densities=new_densities
def VelocityAdvection(deltaTime):
    global velocities
    new_velocities=[None]*width*height
    for y in range(height):
        for x in range(width):
            new_velocities[posToIndex(x,y)]=Vector2(0,0)
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            f=Vector2(x,y)-velocities[posToIndex(x,y)]*deltaTime
            i=f.floor()
            j=f.frac()
            z1=lerp(GetVelocity(y=i.y,x=i.x).x,GetVelocity(y=i.y,x=i.x+1).x,j.x)
            z2=lerp(GetVelocity(y=i.y+1,x=i.x).x,GetVelocity(y=i.y+1,x=i.x+1).x,j.x)
            new_velocities[posToIndex(x,y)].x=lerp(z1,z2,j.y)
            z1=lerp(GetVelocity(y=i.y,x=i.x).y,GetVelocity(y=i.y,x=i.x+1).y,j.x)
            z2=lerp(GetVelocity(y=i.y+1,x=i.x).y,GetVelocity(y=i.y+1,x=i.x+1).y,j.x)
            new_velocities[posToIndex(x,y)].y=lerp(z1,z2,j.y)
    velocities=new_velocities
def posToIndex(x,y):
    return vectToIndex(Vector2(x,y))

def vectToIndex(vector):
    if(isOutOfSim(vector)):
        print("out of sim!")
        return None
    if(isCylinder):
        return vector.y*width+(vector.x%width)
    return vector.y*width+vector.x
def vectToIndexRounded(vector):
    if(isOutOfSim(vector)):
        return None
    if(isCylinder):
        return round(vector.y)*width+round(vector.x)%width
    return round(vector.y)*width+round(vector.x)
def boundVectToIndex(vector):
    if(vector.y==-1):
        if(vector.x<0):
            vector.x=0
        if(vector.x>width-1):
            vector.x=width-1
        return int(vector.x)
    if(vector.y==height):
        if(vector.x<0):
            vector.x=0
        if(vector.x>width-1):
            vector.x=width-1
        return int(vector.x+width+2*height)
    if(vector.x==-1):
        if(vector.y<0):
            vector.y=0
        if(vector.y>height-1):
            vector.y=height-1
        return int(vector.y+width)
    if(vector.x==width):
        if(vector.y<0):
            vector.y=0
        if(vector.y>height-1):
            vector.y=height-1
        return int(vector.y+width+height)
    return None
    

def GetDivergence():
    deltaVelocities=[None]*width*height
    for y in range(height):
        for x in range(width):
            if not isOutOfSim(Vector2(x+1,y)):
                theDelta=velocities[vectToIndex(Vector2(x+1,y))].x/2
            else:theDelta= boundsVelocities[boundVectToIndex(Vector2(x+1,y))].x/2
            if not isOutOfSim(Vector2(x-1,y)):
                theDelta-=velocities[vectToIndex(Vector2(x-1,y))].x/2
            else:theDelta-= boundsVelocities[boundVectToIndex(Vector2(x-1,y))].x/2
            if not isOutOfSim(Vector2(x,y+1)):
                theDelta+=velocities[vectToIndex(Vector2(x,y+1))].y/2
            else:theDelta+= boundsVelocities[boundVectToIndex(Vector2(x,y+1))].y/2
            if not isOutOfSim(Vector2(x,y-1)):
                theDelta-=velocities[vectToIndex(Vector2(x,y-1))].y/2
            else:theDelta-= boundsVelocities[boundVectToIndex(Vector2(x,y-1))].y/2
            deltaVelocities[vectToIndex(Vector2(x,y))]=theDelta
    return deltaVelocities
def clearDivergence():
    deltaVelocities=GetDivergence()
    EqArray=[[] for _ in range(height*width)]
    varsEqArray=[[] for _ in range(height*width)]
    for y in range(height):
        for x in range(width):
            EqArray[posToIndex(x,y)]=[1/4,1/4,1/4,1/4,-deltaVelocities[posToIndex(x,y)]/4]
            varsEqArray[posToIndex(x,y)]=[0,0,0,0]
            for (index,vector) in enumerate(AdjacentVectors):
                resultV=Vector2(x,y)+vector
                if(isOutOfSim(resultV)):
                    EqArray[posToIndex(x,y)][index]=0
                else:
                    varsEqArray[posToIndex(x,y)][index]=vectToIndex(resultV)
    pValues=GaussSeidel(width*height,EqArray,varsEqArray,divergenceAcuracy)
    deltaPValues=[None]*width*height
    for y in range(height):
        for x in range(width):
            theVector=Vector2(0,0)
            if(x+1<width or isCylinder):
                theVector.x+=pValues[vectToIndex(Vector2(x+1,y))]/2
            if(x-1>=0 or isCylinder):
                theVector.x-=pValues[vectToIndex(Vector2(x-1,y))]/2
            if(y+1<height):
                theVector.y+=pValues[vectToIndex(Vector2(x,y+1))]/2
            if(y-1>=0):
                theVector.y-=pValues[vectToIndex(Vector2(x,y-1))]/2
            deltaPValues[vectToIndex(Vector2(x,y))]=theVector
    for y in range(height):
        for x in range(width):
            velocities[posToIndex(x,y)]-=deltaPValues[posToIndex(x,y)]


def dataToString(dataArray):
    txt=""
    for data in dataArray:
        rounded=round(data,2)
        txt+=str(rounded)+"\\"
    return txt
def resetFileAndOpen(isReset,dirTxT):
    if isReset:
        f = open(dirTxT, "w")
        f.write(str(width)+"W"+str(height)+"H")
        f.close()
    return open(dirTxT,"a")

def getDataLen(filePath):
    f=open(filePath,"r")
    filetext=f.read()
    f.close()
    return len(filetext.split("#"))-1

def getDataSetIndexesInDataFile(filePath):
    global width,height
    indexes=[]
    f=open(filePath,"r")
    filetext=f.read()
    if(len(filetext.split("W"))>1):
        filetext=filetext.split("W")
        width=int(filetext[0])
        lenToAdd=len(filetext[0])+1
        filetext=filetext[1]
    if(len(filetext.split("H"))>1):

        filetext=filetext.split("H")
        height=int(filetext[0])
        lenToAdd+=len(filetext[0])+1
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
    return [float(data)/100 for data in dataSet.split("\\")[0:-1]]

def readData(filePath,index=-2):
    global width
    global height
    f=open(filePath,"r")
    filetext=f.read()

    if(len(filetext.split("W"))>1):
        splittedfile=filetext.split("W")
        width=int(splittedfile[0])
        filetext=splittedfile[1]
    if(len(filetext.split("H"))>1):
        splittedfile=filetext.split("H")
        height=int(splittedfile[0])
        filetext=splittedfile[1]
    f.close()
    dataSet=filetext.split("#")[index]
    return [float(data) for data in dataSet.split("\\")[0:-1]]

def applySimulationSettings():
    global numberOfSteps
    global densities
    global boundsVelocities
    global velocities
    numberOfSteps=2000

    densities=createARectangle(densities,Vector2(0*width,50*height)/100,Vector2(99*width,99*height)/100,2)

    velocities=createARectangleByFunc(velocities,Vector2(0*width,0*height)/100,Vector2(99*width,49*height)/100,lambda:Vector2(random.random()*-0+5,0))
    velocities=createARectangleByFunc(velocities,Vector2(0*width,50*height)/100,Vector2(99*width,99*height)/100,lambda:Vector2(random.random()*0-5,0))

    boundsVelocities=createAWall(boundsVelocities,Vector2(0,-1),Vector2(99*width/100,-1),Vector2(5,0),lambda vector: boundVectToIndex(vector))
    boundsVelocities=createAWall(boundsVelocities,Vector2(0*width/100,height),Vector2(99*width/100,height),Vector2(-5,0),lambda vector: boundVectToIndex(vector))

densityF = resetFileAndOpen(isReset or isDensityOnly,"C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/densitydata.txt")
velocityXF = resetFileAndOpen(isReset,"C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityXdata.txt")
velocityYF = resetFileAndOpen(isReset,"C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityYdata.txt")
numberOfSteps=None
if isReset:
    applySimulationSettings()
elif(not isDensityOnly):
    densities=readData("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/densitydata.txt")
    velocityX=readData("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityXdata.txt")
    velocityY=readData("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityYdata.txt")
    velocities=[]
    for (index,data) in enumerate(velocityX):
        velocities.append(Vector2(velocityX[index],velocityY[index]))
    numberOfSteps=2000
if(isDensityOnly and isReset):
    exit("incoherent parameters!")
if(isDensityOnly):
    applySimulationSettings()
    velXDataSetIndexes=getDataSetIndexesInDataFile("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityXdata.txt")
    velYDataSetIndexes=getDataSetIndexesInDataFile("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityYdata.txt")
    frameIndex=0
    while frameIndex<len(velXDataSetIndexes)-1:
        velocityX=readDataInInterval("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityXdata.txt",velXDataSetIndexes[frameIndex]-1,velXDataSetIndexes[frameIndex+1])
        velocityY=readDataInInterval("C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/Data/velocityYdata.txt",velYDataSetIndexes[frameIndex]-1,velYDataSetIndexes[frameIndex+1])
        velocities=[]
        for (index,data) in enumerate(velocityX):
            velocities.append(Vector2(velocityX[index],velocityY[index]))
        DensityDiffusion()
        DensityAdvection(0.1)
        densityF.write(dataToString(densities)+"#")
        if frameIndex%10==0:
            print(round(frameIndex/(len(velXDataSetIndexes)-1)*100,1),"%")
        frameIndex+=1
else:
    start=time.time()
    for index in range(numberOfSteps):
        DensityDiffusion()
        VelocityDiffusion()
        clearDivergence()
        DensityAdvection(0.1)
        VelocityAdvection(0.1)
        clearDivergence()

        """totdiv=0
        while True:
            print(totdiv)
            clearDivergence()
            divergence=GetDivergence()
            totdiv=0
            for div in divergence:
                totdiv+=abs(div)"""
        
        #PrintVelocities()
        #PrintDensities()
        """
        densityF.write(dataToString(densities)+"#")
        velx=[]
        for i in range(len(velocities)):
            velx.append(velocities[i].x)
        vely=[]
        for i in range(len(velocities)):
            vely.append(velocities[i].y)
        velocityXF.write(dataToString(velx)+"#")
        velocityYF.write(dataToString(vely)+"#")"""
        if index%100==0:
            print(round(index/numberOfSteps*100,1),"%")
            print(time.time()-start)
            start=time.time()
#subprocess.call([r'C:/Users/lcach/Documents/4-Ecole/Physique/TM/Navier-Stockes Sim/shutdown.bat'])
    


