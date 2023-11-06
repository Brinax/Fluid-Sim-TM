import math
import random
import time
import numpy
from scipy import interpolate
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

isReset=True
isDensityOnly=False
isCylinder=False


width=20
height=20

if(not isCylinder):
    densities=numpy.zeros((width+2,height+2))
    temperatures=numpy.zeros((width+2,height+2))
    xvelocities=numpy.zeros((width+2,height+2))
    yvelocities=numpy.zeros((width+2,height+2))
else:
    densities=numpy.zeros((width,height+2))
    temperatures=numpy.zeros((width,height+2))
    xvelocities=numpy.zeros((width,height+2))
    yvelocities=numpy.zeros((width,height+2))


AdjacentVectors=[Vector2(1,0),Vector2(-1,0),Vector2(0,-1),Vector2(0,1)]


boundsDensitie=0
densities[0,:]=boundsDensitie
densities[-1,:]=boundsDensitie
densities[:,0]=boundsDensitie
densities[:,-1]=boundsDensitie

densityDiffusion=0
viscosity=2
velocityDiffusionAcuracy=20
diffusionAcuracy=20
divergenceAcuracy=500

thermal_conductivity=0.01
specific_heat_capacity=2
thermal_diffusivity=0.05 #thermal_conductivity/specific_heat_capacity
dilatation_coefficient=0.5
gravity=0.5


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
            posTxt=str(round(xvelocities[posToIndex(x,y)].module()))
            text+=" "+posTxt
        text+="\n"
    print(text)

def GetDensity(x,y):
    if(isCylinder):
        x=x%width
    if(x>width+1):
        x=width+1
    if(x<0):
        x=0
    if(y>height+1):
        y=height+1
    if(y<0):
        y=0
    return densities[x][y]

def GetTemperature(x,y):
    if(isCylinder):
        x=x%width
    if(x>width+1):
        x=width+1
    if(x<0):
        x=0
    if(y>height+1):
        y=height+1
    if(y<0):
        y=0
    return temperatures[x][y]


def GetxVelocity(x,y):
    if(isCylinder):
        x=x%width
    if(x>width+1):
        x=width+1
    if(x<0):
        x=0
    if(y>height+1):
        y=height+1
    if(y<0):
        y=0
    return xvelocities[x][y]
def GetyVelocity(x,y):
    if(isCylinder):
        x=x%width
    if(x>width+1):
        x=width+1
    if(x<0):
        x=0
    if(y>height+1):
        y=height+1
    if(y<0):
        y=0
    return yvelocities[x][y]



def DensityDiffusion():
    global densities
    olddensities=densities.copy()
    if(isCylinder):
        for _ in range(diffusionAcuracy):
            densities[:,1:-1]=(olddensities[:,1:-1]+densityDiffusion*(numpy.roll(densities[:,1:-1],-1,axis=0)+numpy.roll(densities[:,1:-1],1,axis=0)+densities[:,:-2]+densities[:,2:]))/(4*densityDiffusion+1)
    else:
        for _ in range(diffusionAcuracy):
            densities[1:-1,1:-1]=(olddensities[1:-1,1:-1]+densityDiffusion*(densities[:-2,1:-1]+densities[2:,1:-1]+densities[1:-1,:-2]+densities[1:-1,2:]))/(4*densityDiffusion+1)
def TemperatureDiffusion():
    global temperatures
    oldtemperatures=temperatures.copy()
    if(isCylinder):
        for _ in range(diffusionAcuracy):
            temperatures[:,1:-1]=(oldtemperatures[:,1:-1]+thermal_diffusivity*(numpy.roll(temperatures[:,1:-1],-1,axis=0)+numpy.roll(temperatures[:,1:-1],1,axis=0)+temperatures[:,:-2]+temperatures[:,2:]))/(4*thermal_diffusivity+1)
    else:
        for _ in range(diffusionAcuracy):
            temperatures[1:-1,1:-1]=(oldtemperatures[1:-1,1:-1]+thermal_diffusivity*(temperatures[:-2,1:-1]+temperatures[2:,1:-1]+temperatures[1:-1,:-2]+temperatures[1:-1,2:]))/(4*thermal_diffusivity+1)

def VelocityDiffusion():
    global xvelocities,yvelocities
    oldxvelocties=xvelocities.copy()
    oldyvelocties=yvelocities.copy()
    if isCylinder:
        for _ in range(velocityDiffusionAcuracy):
            xvelocities[:,1:-1]=(oldxvelocties[:,1:-1]+viscosity*(numpy.roll(xvelocities[:,1:-1],-1,axis=0)+numpy.roll(xvelocities[:,1:-1],1,axis=0)+xvelocities[:,:-2]+xvelocities[:,2:]))/(4*viscosity+1)
        for _ in range(velocityDiffusionAcuracy):
            yvelocities[:,1:-1]=(oldyvelocties[:,1:-1]+viscosity*(numpy.roll(yvelocities[:,1:-1],-1,axis=0)+numpy.roll(yvelocities[:,1:-1],1,axis=0)+yvelocities[:,:-2]+yvelocities[:,2:]))/(4*viscosity+1)
    else:
        for _ in range(velocityDiffusionAcuracy):
            xvelocities[1:-1,1:-1]=(oldxvelocties[1:-1,1:-1]+viscosity*(xvelocities[:-2,1:-1]+xvelocities[2:,1:-1]+xvelocities[1:-1,:-2]+xvelocities[1:-1,2:]))/(4*viscosity+1)
        for _ in range(velocityDiffusionAcuracy):
            yvelocities[1:-1,1:-1]=(oldyvelocties[1:-1,1:-1]+viscosity*(yvelocities[:-2,1:-1]+yvelocities[2:,1:-1]+yvelocities[1:-1,:-2]+yvelocities[1:-1,2:]))/(4*viscosity+1)
       
def apply_HeatGravity_Influence(deltaTime):
    if(isCylinder):
        yvelocities[:,1:-1]=yvelocities[:,1:-1]-dilatation_coefficient*gravity*temperatures[:,1:-1]*deltaTime
    else:
        yvelocities[1:-1,1:-1]=yvelocities[1:-1,1:-1]-dilatation_coefficient*gravity*temperatures[1:-1,1:-1]*deltaTime


def lerp(a,b,k):
    return a+k*(b-a)


def NumpyAdvection(deltaTime):
    global xvelocities,yvelocities,densities,temperatures

    if(isCylinder):
        x = numpy.arange(0, width+1)
        y = numpy.arange(0, height+2)

        xvelocities_extended = numpy.pad(xvelocities, ((0, 1), (0, 0)), mode='wrap')
        yvelocities_extended = numpy.pad(yvelocities, ((0, 1), (0, 0)), mode='wrap')
        densities_extended = numpy.pad(densities, ((0, 1), (0, 0)), mode='wrap')
        temperatures_extended = numpy.pad(temperatures, ((0, 1), (0, 0)), mode='wrap')


        # Crée un interpolateur pour le champ de vitesse x
        interp_xvelocities = interpolate.RegularGridInterpolator((x,y), xvelocities_extended, method='linear',bounds_error=False,fill_value=None)
        interp_yvelocities = interpolate.RegularGridInterpolator((x,y), yvelocities_extended, method='linear',bounds_error=False,fill_value=None)
        interp_densities = interpolate.RegularGridInterpolator((x,y), densities_extended, method='linear',bounds_error=False,fill_value=None)
        interp_temperatures = interpolate.RegularGridInterpolator((x,y), temperatures_extended, method='linear',bounds_error=False,fill_value=None)
        
        x = numpy.arange(0, width)
        y = numpy.arange(1, height+1)
        X,Y= numpy.meshgrid(x,y)
        X=X.T
        Y=Y.T

        X_new = (X - xvelocities[:, 1:-1] * deltaTime)%width
        Y_new = Y - yvelocities[:, 1:-1] * deltaTime
        
        xvelocities[:,1:-1] = interp_xvelocities(numpy.stack([X_new, Y_new], axis=-1))
        yvelocities[:,1:-1] = interp_yvelocities(numpy.stack([X_new, Y_new], axis=-1))

        densities[:,1:-1] = interp_densities(numpy.stack([X_new, Y_new], axis=-1))
        temperatures[:,1:-1] = interp_temperatures(numpy.stack([X_new, Y_new], axis=-1))
    else:
        exit("numpy advection not defined for non-cylinders!")


def Advection(deltaTime):
    global xvelocities,yvelocities,densities,temperatures
    new_densities=numpy.zeros((width,height))
    new_temperatures=numpy.zeros((width,height))
    new_xvelocities=numpy.zeros((width,height))
    new_yvelocities=numpy.zeros((width,height))
    for y in range(height):
        for x in range(width):
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            if(isCylinder):
                f=Vector2(x-xvelocities[x,y+1]*deltaTime,y+1-yvelocities[x,y+1]*deltaTime)
            else:
                f=Vector2(x+1-xvelocities[x+1,y+1]*deltaTime,y+1-yvelocities[x+1,y+1]*deltaTime)
            i=f.floor()
            j=f.frac()
            z1=lerp(GetxVelocity(i.x,i.y),GetxVelocity(i.x+1,i.y),j.x)
            z2=lerp(GetxVelocity(i.x,i.y+1),GetxVelocity(i.x+1,i.y+1),j.x)

            new_xvelocities[x,y]=lerp(z1,z2,j.y)

            z1=lerp(GetyVelocity(i.x,i.y),GetyVelocity(i.x+1,i.y),j.x)
            z2=lerp(GetyVelocity(i.x,i.y+1),GetyVelocity(i.x+1,i.y+1),j.x)
            new_yvelocities[x,y]=lerp(z1,z2,j.y)

            z1=lerp(GetDensity(i.x,i.y),GetDensity(i.x+1,i.y),j.x)
            z2=lerp(GetDensity(i.x,i.y+1),GetDensity(i.x+1,i.y+1),j.x)
            new_densities[x,y]=lerp(z1,z2,j.y)

            z1=lerp(GetTemperature(i.x,i.y),GetTemperature(i.x+1,i.y),j.x)
            z2=lerp(GetTemperature(i.x,i.y+1),GetTemperature(i.x+1,i.y+1),j.x)
            new_temperatures[x,y]=lerp(z1,z2,j.y)
    if(isCylinder):
        xvelocities[:,1:-1]=new_xvelocities
        yvelocities[:,1:-1]=new_yvelocities
        temperatures[:,1:-1]=new_temperatures
        densities[:,1:-1]=new_densities
    else:
        xvelocities[1:-1,1:-1]=new_xvelocities
        yvelocities[1:-1,1:-1]=new_yvelocities
        temperatures[1:-1,1:-1]=new_temperatures
        densities[1:-1,1:-1]=new_densities

def DensityAdvection(deltaTime):
    global densities
    new_densities=numpy.zeros((width,height))
    for y in range(height):
        for x in range(width):
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            if(isCylinder):
                f=Vector2(x-xvelocities[x,y+1]*deltaTime,y+1-yvelocities[x,y+1]*deltaTime)
            else:
                f=Vector2(x+1-xvelocities[x+1,y+1]*deltaTime,y+1-yvelocities[x+1,y+1]*deltaTime)
            i=f.floor()
            j=f.frac()
            z1=lerp(GetDensity(i.x,i.y),GetDensity(i.x+1,i.y),j.x)
            z2=lerp(GetDensity(i.x,i.y+1),GetDensity(i.x+1,i.y+1),j.x)
            new_densities[x,y]=lerp(z1,z2,j.y)
    if(isCylinder):
        densities[:,1:-1]=new_densities
    else:
        densities[1:-1,1:-1]=new_densities

def TemperatureAdvection(deltaTime):
    global temperatures
    new_temperatures=numpy.zeros((width,height))
    for y in range(height):
        for x in range(width):
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            if(isCylinder):
                f=Vector2(x-xvelocities[x,y+1]*deltaTime,y+1-yvelocities[x,y+1]*deltaTime)
            else:
                f=Vector2(x+1-xvelocities[x+1,y+1]*deltaTime,y+1-yvelocities[x+1,y+1]*deltaTime)
            i=f.floor()
            j=f.frac()
            z1=lerp(GetTemperature(i.x,i.y),GetTemperature(i.x+1,i.y),j.x)
            z2=lerp(GetTemperature(i.x,i.y+1),GetTemperature(i.x+1,i.y+1),j.x)
            new_temperatures[x,y]=lerp(z1,z2,j.y)
    if(isCylinder):
        temperatures[:,1:-1]=new_temperatures
    else:
        temperatures[1:-1,1:-1]=new_temperatures
        

def VelocityAdvection(deltaTime):
    global xvelocities,yvelocities
    new_xvelocities=numpy.zeros((width,height))
    new_yvelocities=numpy.zeros((width,height))
    for y in range(height):
        for x in range(width):
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            if(isCylinder):
                f=Vector2(x-xvelocities[x,y+1]*deltaTime,y+1-yvelocities[x,y+1]*deltaTime)
            else:
                f=Vector2(x+1-xvelocities[x+1,y+1]*deltaTime,y+1-yvelocities[x+1,y+1]*deltaTime)
            i=f.floor()
            j=f.frac()
            z1=lerp(GetxVelocity(i.x,i.y),GetxVelocity(i.x+1,i.y),j.x)
            z2=lerp(GetxVelocity(i.x,i.y+1),GetxVelocity(i.x+1,i.y+1),j.x)

            new_xvelocities[x,y]=lerp(z1,z2,j.y)

            z1=lerp(GetyVelocity(i.x,i.y),GetyVelocity(i.x+1,i.y),j.x)
            z2=lerp(GetyVelocity(i.x,i.y+1),GetyVelocity(i.x+1,i.y+1),j.x)
            new_yvelocities[x,y]=lerp(z1,z2,j.y)
    if(isCylinder):
        xvelocities[:,1:-1]=new_xvelocities
        yvelocities[:,1:-1]=new_yvelocities
    else:
        xvelocities[1:-1,1:-1]=new_xvelocities
        yvelocities[1:-1,1:-1]=new_yvelocities
def posToIndex(x,y):
    return vectToIndex(Vector2(x,y))

def vectToIndex(vector):
    if(isOutOfSim(vector)):
        print("out of sim!")
        return None
    if(isCylinder):
        return (vector.x%width+1),vector.y+1
    return vector.x+1,vector.y+1
def vectToIndexRounded(vector):
    if(isOutOfSim(vector)):
        return None
    if(isCylinder):
        return round(vector.x)%width,round(vector.y)+1
    return round(vector.x)+1,round(vector.y)+1
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
    if(isCylinder):
        deltaVelocities=(numpy.roll(xvelocities[:,1:-1],-1,axis=0)-numpy.roll(xvelocities[:,1:-1],1,axis=0)+yvelocities[:,2:]-yvelocities[:,:-2])/2
    else:
        deltaVelocities=(xvelocities[2:,1:-1]-xvelocities[:-2,1:-1]+yvelocities[1:-1,2:]-yvelocities[1:-1,:-2])/2
    return deltaVelocities


def clearAccuratlyDivergence(maxdiv):
    global divergenceCount
    maxdivergence=100
    while(abs(maxdivergence)>abs(maxdiv)):
        divergenceCount+=1
        clearDivergence()
        maxdivergence=0
        for divergencearray in GetDivergence():
            for divergence in divergencearray:
                if(abs(maxdivergence)<abs(divergence)):
                    maxdivergence=divergence
        print(maxdivergence)
def clearDivergence(overrelax=1):
    deltaVelocities=GetDivergence()
    pValues=numpy.zeros((width,height))
    if(isCylinder):
        for _ in range(divergenceAcuracy):
            oldpValues=pValues.copy()
            pValues[:,1:-1]=overrelax*((numpy.roll(pValues[:, 1:-1],1,axis=0)+numpy.roll(pValues[:, 1:-1],-1,axis=0)+pValues[:, :-2]+pValues[:, 2:])-deltaVelocities[:, 1:-1])/4 +(1-overrelax)*oldpValues[:,1:-1]

            pValues[:, 0]=overrelax*((numpy.roll(pValues[:, 0],1,axis=0)+numpy.roll(pValues[:, 0],-1,axis=0)+ pValues[:,1])-deltaVelocities[:, 0])/3+(1-overrelax)*oldpValues[:,0]
            pValues[:, -1]=overrelax*((numpy.roll(pValues[:, -1],1,axis=0)+numpy.roll(pValues[:, -1],-1,axis=0)+ pValues[:,-2])-deltaVelocities[:, -1])/3+(1-overrelax)*oldpValues[:,-1]

            #pValues=newpValues*(overrelax+1)-overrelax*pValues
            #pValues=newpValues

        xvelocities[:,1:-1]=xvelocities[:,1:-1]-(numpy.roll(pValues,-1,axis=0)-numpy.roll(pValues,1,axis=0))/2

        yvelocities[:,2:-2]=yvelocities[:,2:-2]-(pValues[:,2:]-pValues[:,:-2])/2

        yvelocities[:, 1]=yvelocities[:,1]-(pValues[:,1])/2
        yvelocities[:, -2]=yvelocities[:,-2]-(-pValues[:,-2])/2
    else:
        newpValues=pValues.copy()
        for _ in range(divergenceAcuracy):
            newpValues[1:-1,1:-1]=((pValues[:-2, 1:-1]+pValues[2:, 1:-1]+pValues[1:-1, :-2]+pValues[1:-1, 2:])-deltaVelocities[1:-1, 1:-1])/4

            newpValues[0, 1:-1]=((pValues[1, 1:-1] +pValues[0, :-2]+pValues[0,2:])-deltaVelocities[0, 1:-1])/4
            newpValues[-1, 1:-1]=((pValues[-2, 1:-1] +pValues[-1, :-2]+pValues[-1,2:])-deltaVelocities[-1, 1:-1])/4

            newpValues[1:-1, 0]=((pValues[:-2, 0]+pValues[2:, 0]+ pValues[1:-1,1])-deltaVelocities[1:-1, 0])/4
            newpValues[1:-1, -1]=((pValues[:-2, -1]+pValues[2:, -1]+ pValues[1:-1,-2])-deltaVelocities[1:-1, -1])/4

            newpValues[0,0]=(pValues[1,0]+pValues[0,1]-deltaVelocities[0, 0])/4
            newpValues[-1,0]=(pValues[-2,0]+pValues[-1,1]-deltaVelocities[-1, 0])/4
            newpValues[0,-1]=(pValues[1,-1]+pValues[0,-2]-deltaVelocities[0, -1])/4
            newpValues[-1,-1]=(pValues[-2,-1]+pValues[-1,-2]-deltaVelocities[-1, -1])/4
            pValues=newpValues.copy()

        xvelocities[2:-2,1:-1]=xvelocities[2:-2,1:-1]-(pValues[2:,:]-pValues[:-2,:])/2
        yvelocities[1:-1,2:-2]=yvelocities[1:-1,2:-2]-(pValues[:,2:]-pValues[:,:-2])/2



        xvelocities[1, 1:-1]=xvelocities[1,1:-1]-(pValues[1,:])/2
        xvelocities[-2, 1:-1]=xvelocities[-2,1:-1]-(-pValues[-2,:])/2

        yvelocities[1:-1, 1]=yvelocities[1:-1,1]-(pValues[:,1])/2
        yvelocities[1:-1, -2]=yvelocities[1:-1,-2]-(-pValues[:,-2])/2

    


def dataToString(dataArray):
    txt=""
    if(isCylinder):
        cuttedArray=dataArray[:,1:-1]
    else:
        cuttedArray=dataArray[1:-1,1:-1]
    for y in range(height):
        for x in range(width):
            rounded=round(cuttedArray[x,y],2)
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



    indexes.append(lenToAdd)
    for i,c in enumerate(filetext):
        if(c=="#"):
            indexes.append(i+lenToAdd+2)
    return indexes

def readDataInInterval(filePath,startIndex,endIndex):
    f=open(filePath,"r")
    filetext=f.read()
    dataSet=filetext[startIndex:endIndex]
    return [float(data) for data in dataSet.split("\\")[0:-1]]

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
    global xvelocities,yvelocities
    numberOfSteps=1

    densities=createARectangle(densities,Vector2(0,height*3/4),Vector2(width-1,height-1),2)
    densities=createARectangle(densities,Vector2(0,0),Vector2(width-1,height/4),2)
    #densities=createARectangle(densities,Vector2(0,height*4/10),Vector2(width-1,height*6/10),2)

    """xvelocities=createARectangleByFunc(xvelocities,Vector2(0,0),Vector2(width-1,height/2),lambda:random.random()*-1+5)
    xvelocities[:,0]=5
    xvelocities=createARectangleByFunc(xvelocities,Vector2(0,height/2),Vector2(width-1,height-1),lambda:random.random()*1-5)
    xvelocities[:,-1]=-5"""

    xvelocities=createARectangleByFunc(xvelocities,Vector2(0,0),Vector2(width-1,height-1),lambda:random.random()*0.00001-0.000005)
    #yvelocities=createARectangle(xvelocities,Vector2(0,0),Vector2(width-1,height/2),1.0)
    #yvelocities=createARectangle(xvelocities,Vector2(0,height/2),Vector2(width-1,height-1),1.0)
    yvelocities[10,10]=0.5
    yvelocities[10,11]=0.5
    yvelocities[11,10]=0.5
    yvelocities[11,11]=0.5

    temperatures[:,0]=-1
    temperatures[:,-1]=1


densityF = resetFileAndOpen(isReset or isDensityOnly,"Navier-Stockes Sim/Data/densitydata.txt")
temperatureF = resetFileAndOpen(isReset,"Navier-Stockes Sim/Data/temperaturedata.txt")
velocityXF = resetFileAndOpen(isReset,"Navier-Stockes Sim/Data/velocityXdata.txt")
velocityYF = resetFileAndOpen(isReset,"Navier-Stockes Sim/Data/velocityYdata.txt")
numberOfSteps=None
divergenceCount=0
if isReset:
    applySimulationSettings()
elif(not isDensityOnly):
    densities=readData("Navier-Stockes Sim/Data/densitydata.txt")
    velocityX=readData("Navier-Stockes Sim/Data/velocityXdata.txt")
    velocityY=readData("Navier-Stockes Sim/Data/velocityYdata.txt")
    velocities=[]
    for (index,data) in enumerate(velocityX):
        velocities.append(Vector2(velocityX[index],velocityY[index]))
    numberOfSteps=3000
if(isDensityOnly and isReset):
    exit("incoherent parameters!")
if(isDensityOnly):
    applySimulationSettings()
    velXDataSetIndexes=getDataSetIndexesInDataFile("Navier-Stockes Sim/Data/velocityXdata.txt")
    velYDataSetIndexes=getDataSetIndexesInDataFile("Navier-Stockes Sim/Data/velocityYdata.txt")
    frameIndex=0
    while frameIndex<len(velXDataSetIndexes)-1:
        velocityX=readDataInInterval("Navier-Stockes Sim/Data/velocityXdata.txt",velXDataSetIndexes[frameIndex],velXDataSetIndexes[frameIndex+1])
        velocityY=readDataInInterval("Navier-Stockes Sim/Data/velocityYdata.txt",velYDataSetIndexes[frameIndex],velYDataSetIndexes[frameIndex+1])
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
    deltaTime=0.2
    viscosity*=deltaTime
    densityDiffusion*=deltaTime
    thermal_diffusivity*=deltaTime
    totstart=time.time()
    for index in range(numberOfSteps):
        DensityDiffusion()
        TemperatureDiffusion()
        VelocityDiffusion()
        #clearDivergence()
        clearAccuratlyDivergence(0.01)
        NumpyAdvection(0.1)
        #clearAccuratlyDivergence(0.0001)
        clearAccuratlyDivergence(0.01)
        apply_HeatGravity_Influence(deltaTime)
        clearAccuratlyDivergence(0.01)
        if(index%1==0):
            if(isCylinder):
                numpy.savetxt(densityF,densities[:,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
                numpy.savetxt(temperatureF,temperatures[:,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
                numpy.savetxt(velocityXF,xvelocities[:,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
                numpy.savetxt(velocityYF,yvelocities[:,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
            else:
                numpy.savetxt(densityF,densities[1:-1,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
                numpy.savetxt(temperatureF,temperatures[1:-1,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
                numpy.savetxt(velocityXF,xvelocities[1:-1,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
                numpy.savetxt(velocityYF,yvelocities[1:-1,1:-1].T,delimiter="\\",newline="\\",fmt="%.2f")
            densityF.write("#")
            temperatureF.write("#")
            velocityYF.write("#")
            velocityXF.write("#")

            if index%1==0:
                print(round(index/numberOfSteps*100,2),"%")
                print(divergenceCount)
                divergenceCount=0
                print("tottime",time.time()-totstart)
                totstart=time.time()
    

#print(divergenceCount/numberOfSteps)
