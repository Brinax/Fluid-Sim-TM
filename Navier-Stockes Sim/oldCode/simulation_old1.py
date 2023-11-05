import math

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
    def module(self):
        return math.sqrt(self.x**2+self.y**2)


width=50
height=50
densities=[1]*width*height
velocities=[]
AdjacentVectors=[Vector2(1,0),Vector2(-1,0),Vector2(0,-1),Vector2(0,1)]
for _ in range(width*height):
    velocities.append(Vector2(0,0))
boundsDensitie=1
boundsVelocitie=Vector2(x=-10,y=0)
diffusionConst=0.5
diffusionAcuracy=10
divergenceAcuracy=10

def isOutOfSim(Vector):
    x=Vector.x
    y=Vector.y
    if(x<0 or x>=width or y<0 or y>=height):
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

def GetAdjacentCases(x,y):
    AdjacentCases=[0]*4
    AdjacentCases[0]=y*width+x+1
    AdjacentCases[1]=y*width+x-1
    AdjacentCases[2]=(y+1)*width+x
    AdjacentCases[3]=(y-1)*width+x
    return AdjacentCases
def GetDensity(x,y):
    if(x<0 or x>=width or y<0 or y>=height):
        return boundsDensitie
    else:
        return densities[y*width+x]

def UpdateDensities():
    global densities
    #matriceToSolve=[0]*((height*width)**2)
    EqArray=[None]*width*height
    varsEqArray=[[0,0,0,0] for _ in range(height*width)]

    for y in range(height):
        for x in range(width):
            varsFactor=diffusionConst/((1+diffusionConst)*4)
            EqArray[posToIndex(x,y)]=[varsFactor,varsFactor,varsFactor,varsFactor,densities[y*width+x]/(1+diffusionConst)]
            for (index,vector) in enumerate(AdjacentVectors):
                resultV=Vector2(x,y)+vector
                if(isOutOfSim(resultV)):
                    EqArray[posToIndex(x,y)][index]=0
                else:
                    varsEqArray[posToIndex(x,y)][index]=vectToIndex(resultV)

    densities = GaussSeidel(width*height,EqArray,varsEqArray,diffusionAcuracy)

#in Eq arrays la dérnière valeur de chaque chaîne doit être la constante dans l'équation
def GaussSeidel(numbOfVars,EqArrays,varsEqArrays,numbOfIterations):
    solvedVariables=[0]*numbOfVars
    #newsolvedVariables=[0]*numbOfVars not jacobi!
    for _ in range(numbOfIterations):
        for i in range(numbOfVars):
            varAnsw=EqArrays[i][len(EqArrays[i])-1]
            for i2 in range(len(EqArrays[i])-1):
                varAnsw+=solvedVariables[varsEqArrays[i][i2]]*EqArrays[i][i2]
            solvedVariables[i]=varAnsw
    return solvedVariables


def matriceSolver(values,matrice,height,numbOfIterations):
    if len(matrice)!=height**2:
        print("matrice length doesn't correspond!")
        exit()
    #gauss-seidel
    nonzeroVarsInMatr=[set() for _ in range(height)]
    for i in range(height):
        for i2 in range(height):
            if(matrice[i*height+i2]!=0):
                nonzeroVarsInMatr[i].add(i2)
    solvedVariables=[0]*height
    newsolvedVariables=[0]*height
    for _ in range(numbOfIterations):
        for i in range(height):
            coef=matrice[i*height+i]
            varAnsw=values[i]/coef
            for i2 in nonzeroVarsInMatr[i]:
                if(i2!=i):
                    varAnsw+=-matrice[i*height+i2]*solvedVariables[i2]/coef
            newsolvedVariables[i]=varAnsw
        solvedVariables=newsolvedVariables
    return solvedVariables
def lerp(a,b,k):
    return a+k*(b-a)

def Advection(deltaTime):
    global densities
    new_densities=[None]*width*height
    for y in range(height):
        for x in range(width):
            #point d'ou viennent les valeurs selon la vitesse pour la prochaine frame
            f=Vector2(x,y)-velocities[y*width+x]*deltaTime
            i=f.floor()
            j=f.frac()
            z1=lerp(GetDensity(y=round(i.y),x=round(i.x)),GetDensity(y=round(i.y),x=round(i.x)+1),j.x)
            z2=lerp(GetDensity(y=round(i.y)+1,x=round(i.x)),GetDensity(y=round(i.y)+1,x=round(i.x)+1),j.x)
            new_densities[y*width+x]=lerp(z1,z2,j.y)
    densities=new_densities
def posToIndex(x,y):
    return vectToIndex(Vector2(x,y))
def vectToIndex(vector):
    if(isOutOfSim(vector)):
        return None
    return vector.y*width+vector.x
def clearDivergence():
    deltaVelocities=[None]*width*height
    
    for y in range(height):
        for x in range(width):
            if not isOutOfSim(Vector2(x+1,y)):
                theDelta=velocities[vectToIndex(Vector2(x+1,y))].x/2
            else:theDelta=boundsVelocitie.x/2
            if not isOutOfSim(Vector2(x-1,y)):
                theDelta-=velocities[vectToIndex(Vector2(x-1,y))].x/2
            else:theDelta-=boundsVelocitie.x/2
            if not isOutOfSim(Vector2(x,y+1)):
                theDelta+=velocities[vectToIndex(Vector2(x,y+1))].y/2
            else:theDelta+= boundsVelocitie.y/2
            if not isOutOfSim(Vector2(x,y-1)):
                theDelta-=velocities[vectToIndex(Vector2(x,y-1))].y/2
            else:
                theDelta-=boundsVelocitie.y/2
            deltaVelocities[vectToIndex(Vector2(x,y))]=theDelta
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
            if(x+1<width):
                theVector.x+=pValues[vectToIndex(Vector2(x+1,y))]/2
            if(x-1>=0):
                theVector.x-=pValues[vectToIndex(Vector2(x-1,y))]/2
            if(y+1<height):
                theVector.y+=pValues[vectToIndex(Vector2(x,y+1))]/2
            if(y-1>=0):
                theVector.y-=pValues[vectToIndex(Vector2(x,y-1))]/2
            deltaPValues[vectToIndex(Vector2(x,y))]=theVector
    for y in range(height):
        for x in range(width):
            velocities[vectToIndex(Vector2(x,y))]-=deltaPValues[vectToIndex(Vector2(x,y))]

def dataToString(dataArray):
    txt=""
    for data in dataArray:
        rounded=round(data,2)
        txt+=str(rounded)+"\\"
    return txt
    
f = open("Navier-Stockes Sim/Data/densitydata.txt", "w")
f.write(str(width)+"W")
f.close()
f = open("Navier-Stockes Sim/Data/velocitydata.txt", "w")
f.write(str(width)+"W")
f.close()

densityF = open("Navier-Stockes Sim/Data/densitydata.txt", "a")
velocityF = open("Navier-Stockes Sim/Data/velocitydata.txt", "a")

numberOfSteps=100
for index in range(numberOfSteps):
    UpdateDensities()
    Advection(0.1)
    clearDivergence()
    #PrintVelocities()
    #PrintDensities()
    densityF.write(dataToString(densities)+"#")
    velModules=[]
    for i in range(len(velocities)):
        velModules.append(velocities[i].module())
    velocityF.write(dataToString(velModules)+"#")
    if index%10==0:
        print(index/numberOfSteps*100,"%")
    


