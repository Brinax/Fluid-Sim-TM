# Importation des bibliothèques nécessaires
import numpy                       
from matplotlib import pyplot      
import time, sys                   

# Paramètres de la grille
gridxdim = 41
dx = 2 / (gridxdim-1)
numberOfSteps = 25 
dt = .025
c = 1     

# Initialisation des conditions initiales
u = numpy.ones(gridxdim)
u[int(.5 / dx):int(1 / dx + 1)] = 2

# Affichage des conditions initiales
pyplot.plot(numpy.linspace(0, 2, gridxdim), u)
pyplot.show()

# Initialisation d'un tableau temporaire
un = numpy.ones(gridxdim)

# Boucle pour avancer dans le temps
for n in range(numberOfSteps):  
    un = u.copy() 
    for i in range(1,gridxdim): 
        u[i] = un[i] - un[i] * dt / dx * (un[i] - un[i-1]) 

# Affichage du résultat
pyplot.plot(numpy.linspace(0, 2, gridxdim), u)
pyplot.show()
