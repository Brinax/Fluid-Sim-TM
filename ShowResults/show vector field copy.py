import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import block_reduce
import math
from matplotlib.colors import LinearSegmentedColormap

width=-1
height=-1
def getDataSetIndexesInDataFile(filePath):
    global width,height
    indexes=[]
    f=open(filePath,"r")
    filetext=f.read()
    if(len(filetext.split("W"))>1):
        filetext=filetext.split("W")
        width=int(filetext[0])
        height=width
        lenToAdd=len(filetext[0])+1
        filetext=filetext[1]
    if(len(filetext.split("H"))>1):

        filetext=filetext.split("H")
        height=int(filetext[0])
        lenToAdd+=len(filetext[0])+1
        filetext=filetext[1]


    if(filetext[len(filetext)-1]!="#"):
        filetext+="#"
    indexes.append(lenToAdd)
    for i,c in enumerate(filetext):
        if(c=="#"):
            indexes.append(i+lenToAdd+1)
    return indexes

def sign(x):
    if x<0:
        return -1
    return 1
def mod(x):
    if(x==0):
        return 0
    return x/abs(x)
def readDataInInterval(filePath,startIndex,endIndex):
    f=open(filePath,"r")
    filetext=f.read()
    dataSet=filetext[startIndex:endIndex]
    return [float(data) for data in dataSet.split("\\")[0:-1]]




velXDataSetIndexes=getDataSetIndexesInDataFile("ShowResults/xVelParticle copy.txt")
velYDataSetIndexes=getDataSetIndexesInDataFile("ShowResults/yVelParticle copy.txt")
#DensityDataSetIndexes=getDataSetIndexesInDataFile("ShowResults/densitydata2.txt")
frameIndex=0
print(len(velXDataSetIndexes))

u=readDataInInterval("ShowResults/xVelParticle copy.txt",velXDataSetIndexes[frameIndex],velXDataSetIndexes[frameIndex+1])
v=readDataInInterval("ShowResults/yVelParticle copy.txt",velYDataSetIndexes[frameIndex],velYDataSetIndexes[frameIndex+1])
#d=readDataInInterval("ShowResults/densitydata2.txt",DensityDataSetIndexes[frameIndex],DensityDataSetIndexes[frameIndex+1])



u=np.array(u)
v=np.array(v)
#d=np.array(d)

# Redimensionner les composantes pour correspondre à une grille 2x2
u = u.reshape(height, width)
v = v.reshape(height, width)
#d = d.reshape(height, width)
u=np.flipud(u)
v=np.flipud(v)
v=-v
# Créer une grille de points pour les positions des vecteurs
x_indices = np.arange(width)
y_indices = np.arange(height)
x, y = np.meshgrid(x_indices, y_indices)

block_size = (5, 5)
u = block_reduce(u, block_size, np.mean)
v = block_reduce(v, block_size, np.mean)
x = block_reduce(x, block_size, np.mean)
y = block_reduce(y, block_size, np.mean)


colors_rgb = [(0, 0, 0),    # noir
              (0, 0, 1),    # bleu
              (0, 1, 0),    # vert
              (1, 0, 0),    # rouge
              (1, 1, 1)] 
nodes = [0.0, 0.25, 0.5, 0.75, 1.0]
cmap_custom = LinearSegmentedColormap.from_list("custom", list(zip(nodes, colors_rgb)))
"""d = np.tanh(d * 2.0 - 1.0) / np.tanh(1.0)
d = np.tanh(d) / np.tanh(1.0)
d = np.tanh(d) / np.tanh(1.0)
d = d / 2.0 + 0.5"""
#d_normalized = (d - np.min(d)) / (np.max(d) - np.min(d))

# Afficher la densité en arrière-plan
#plt.imshow(d_normalized, cmap=cmap_custom, extent=[-0.5, width-0.5, -0.5, height-0.5])

norm = np.sqrt(u**2 + v**2)
colors = u
u = u / norm
v = v / norm

# Normalisez les valeurs pour qu'elles se situent entre 0 et 1
print(np.min(colors),np.max(colors))
colors = (colors - np.min(colors)) / (np.max(colors) - np.min(colors))
x = x.astype(np.float64)
y = y.astype(np.float64)
x-=u*2.5
y-=v*2.5
# Utilisez la colormap coolwarm pour convertir les valeurs normalisées en couleurs
colors = plt.cm.binary(colors)
plt.quiver(x.flatten(), y.flatten(), u.flatten(), v.flatten(), color=colors.reshape(-1, 4), scale=10,linewidths=1)
           #headlength=0, headwidth=0, headaxislength=0)
plt.gca().set_xticks([])
plt.gca().set_yticks([])
plt.xlim(-0.5, width-0.5)
plt.ylim(-0.5, height-0.5)
plt.gca().set_aspect('equal', adjustable='box')

plt.show()

