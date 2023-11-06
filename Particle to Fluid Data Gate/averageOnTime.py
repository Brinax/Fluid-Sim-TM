

width=100
height=30

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
    return [float(data) for data in dataSet.split("\\")[0:-1]]
def resetFileAndOpen(isReset,dirTxT):
    if isReset:
        f = open(dirTxT, "w")
        f.write(str(width)+"W"+str(height)+"H")
        f.close()
    return open(dirTxT,"a")
def dataToString(dataArray):
    txt=""
    for data in dataArray:
        rounded=round(data,2)
        txt+=str(rounded)+"\\"
    return txt

densityAVF = resetFileAndOpen(True,"Particle to Fluid Data Gate/densitiesAV.txt")
velocityXAVF = resetFileAndOpen(True,"Particle to Fluid Data Gate/xVelParticleAV.txt")
velocityYAVF = resetFileAndOpen(True,"Particle to Fluid Data Gate/yVelParticleAV.txt")


densitiesDataSetIndexes=getDataSetIndexesInDataFile("Particle to Fluid Data Gate/densities.txt")
velXDataSetIndexes=getDataSetIndexesInDataFile("Particle to Fluid Data Gate/xVelParticle.txt")
velYDataSetIndexes=getDataSetIndexesInDataFile("Particle to Fluid Data Gate/yVelParticle.txt")
frameIndex=0
while frameIndex<len(velXDataSetIndexes)-5:
    densities=[]
    velocityX=[]
    velocityY=[]
    for index in range(5):
        densities.append(readDataInInterval("Particle to Fluid Data Gate/densities.txt",densitiesDataSetIndexes[frameIndex+index]-1,densitiesDataSetIndexes[frameIndex+index+1]))
        velocityX.append(readDataInInterval("Particle to Fluid Data Gate/xVelParticle.txt",velXDataSetIndexes[frameIndex+index]-1,velXDataSetIndexes[frameIndex+index+1]))
        velocityY.append(readDataInInterval("Particle to Fluid Data Gate/yVelParticle.txt",velYDataSetIndexes[frameIndex+index]-1,velYDataSetIndexes[frameIndex+index+1]))
    newdensities=[]
    newvelocityX=[]
    newvelocityY=[]
    for index in range(len(densities[0])):
        newdensities.append((densities[0][index]+densities[1][index]+densities[2][index]+densities[3][index]+densities[4][index])/5)
        newvelocityX.append((velocityX[0][index]+velocityX[1][index]+velocityX[2][index]+velocityX[3][index]+velocityX[4][index])/5)
        newvelocityY.append((velocityY[0][index]+velocityY[1][index]+velocityY[2][index]+velocityY[3][index]+velocityY[4][index])/5)

    densityAVF.write(dataToString(newdensities)+"#")
    velocityXAVF.write(dataToString(newvelocityX)+"#")
    velocityYAVF.write(dataToString(newvelocityY)+"#")
    if frameIndex%10==0:
        print(round(frameIndex/(len(velXDataSetIndexes)-1)*100,1),"%")
    frameIndex+=1
    
        

