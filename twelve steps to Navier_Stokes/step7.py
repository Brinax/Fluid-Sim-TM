import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from time import *

nx = 31
ny = 31
nt = 10

v=.05
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
dt = .25*dx*dy/v


x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((nx, ny))
un = numpy.ones((nx, ny))

u[int(.5 / dy):int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

fig = pyplot.figure(figsize=(11, 7), dpi=100)
ax = fig.add_subplot(111, projection='3d')
X, Y = numpy.meshgrid(x, y)
surface = [ax.plot_surface(X, Y, u, cmap=cm.viridis, rstride=2, cstride=2)]

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')


def update(i):
    global u,nt,v
    startTime=time()
    for _ in range(nt):
        un=u+v*dt*((numpy.roll(u,-1,axis=0)-2*u+numpy.roll(u,1,axis=0))/dx**2
                   +(numpy.roll(u,-1,axis=1)-2*u+numpy.roll(u,1,axis=1))/dy**2)
        u = un.copy()
    print("simtime:",time()-startTime)
    startTime=time()
    surface[0].remove()
    surface[0] = ax.plot_surface(X, Y, u, cmap=cm.viridis, rstride=2, cstride=2)
    print("showtime:",time()-startTime)

ani = FuncAnimation(fig, update, frames=nt, interval=50)

pyplot.show()
