particleDataPath="C:/Users/lcach/Documents/4-Ecole/Physique/TM/Particle to Fluid Data Gate/data.txt"
xVelOutputPath="C:/Users/lcach/Documents/4-Ecole/Physique/TM/Particle to Fluid Data Gate/xVelParticle.txt"
yVelOutputPath="C:/Users/lcach/Documents/4-Ecole/Physique/TM/Particle to Fluid Data Gate/yVelParticle.txt"
densityOutputPath="C:/Users/lcach/Documents/4-Ecole/Physique/TM/Particle to Fluid Data Gate/densities.txt"
energyOutputPath="C:/Users/lcach/Documents/4-Ecole/Physique/TM/Particle to Fluid Data Gate/energies.txt"
xInputSize=100
yInputSize=30

xOutputGridSize=100
yOutputGridSize=30

xInputSize+=xInputSize/xOutputGridSize
yInputSize+=yInputSize/yOutputGridSize

#pour des particules ayant toutes la même masse

def getRoundIndex(xPos,yPos):

    xPos=round(xPos*xOutputGridSize/xInputSize)
    yPos=round(yPos*yOutputGridSize/yInputSize)
    return yPos*xOutputGridSize+xPos


def getParticleData(particlePath,xVelOutputPath,yVelOutputPath,densityOutputPath,energyOutPutPath):
    datatxt=open(particlePath,"r").read()

    xVelOutput= open(xVelOutputPath,"w")
    xVelOutput.write("")
    xVelOutput.close()
    xVelOutput=open(xVelOutputPath,"a")
    xVelOutput.write(str(xOutputGridSize)+"W"+str(yOutputGridSize)+"H")
    
    yVelOutput= open(yVelOutputPath,"w")
    yVelOutput.write("")
    yVelOutput.close()
    yVelOutput=open(yVelOutputPath,"a")
    yVelOutput.write(str(xOutputGridSize)+"W"+str(yOutputGridSize)+"H")
    
    densityOutput= open(densityOutputPath,"w")
    densityOutput.write("")
    densityOutput.close()
    densityOutput=open(densityOutputPath,"a")
    densityOutput.write(str(xOutputGridSize)+"W"+str(yOutputGridSize)+"H")

    energyOutput= open(energyOutPutPath,"w")
    energyOutput.write("")
    energyOutput.close()
    energyOutput=open(energyOutPutPath,"a")
    energyOutput.write(str(xOutputGridSize)+"W"+str(yOutputGridSize)+"H")

    FramesData=datatxt[1:].split("!")
    for (frameIndex,frameData) in enumerate(FramesData):
        
        gridxVel=[0]*xOutputGridSize*yOutputGridSize
        gridyVel=[0]*xOutputGridSize*yOutputGridSize
        gridDensities=[0]*xOutputGridSize*yOutputGridSize
        gridEnergy=[0]*xOutputGridSize*yOutputGridSize

        gridDens=[0]*xOutputGridSize*yOutputGridSize

        FramesData[frameIndex]=frameData[1:].split("#")

        for (ballIndex,ballData) in enumerate(FramesData[frameIndex]):
            posData=ballData[ballData.index("p")+1:ballData.index("v")].split('x')
            posData=[float(numb) for numb in posData]
            velData=ballData[ballData.index("v")+1:ballData.index("m")].split('x')
            velData=[float(numb) for numb in velData]
            GridIndex=getRoundIndex(posData[0],posData[1])
            gridxVel[GridIndex]=(gridxVel[GridIndex]*gridDens[GridIndex]+velData[0])/(gridDens[GridIndex]+1)
            gridyVel[GridIndex]=(gridyVel[GridIndex]*gridDens[GridIndex]+velData[1])/(gridDens[GridIndex]+1)
            if(ballIndex>4860):
                gridDensities[GridIndex]+=1
            gridDens[GridIndex]+=1
            gridEnergy[GridIndex]+=(velData[0]**2+velData[1]**2)**(0.5)


        for index in range(xOutputGridSize*yOutputGridSize):
            xVelOutput.write(str(round(gridxVel[index],2))+"\\")
            yVelOutput.write(str(round(gridyVel[index],2))+"\\")
            densityOutput.write(str(round(gridDensities[index],2))+"\\")
            energyOutput.write(str(round(gridEnergy[index],2))+"\\")

        xVelOutput.write("#")
        yVelOutput.write("#")
        densityOutput.write("#")
        energyOutput.write("#")
        print(frameIndex)
        



if __name__=="__main__":
    getParticleData(particleDataPath,xVelOutputPath,yVelOutputPath,densityOutputPath,energyOutputPath)


