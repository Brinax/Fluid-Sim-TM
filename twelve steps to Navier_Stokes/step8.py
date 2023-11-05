import numpy
from matplotlib import pyplot, cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from time import *

nx = 41
ny = 41
nt = 120

nu=.001
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma=.0009
dt = sigma*dx*dy/nu


x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((nx, ny))
v = numpy.ones((nx, ny))

u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 
v[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2

fig = pyplot.figure(figsize=(11, 7), dpi=100)
ax = fig.add_subplot(111, projection='3d')
X, Y = numpy.meshgrid(x, y)
surface = [ax.plot_surface(X, Y, u, cmap=cm.viridis, rstride=2, cstride=2)]

ax.set_xlabel('$x$')
ax.set_ylabel('$y$')


def update(i):
    global v,u,nt,nu
    startTime=time()
    for _ in range(nt):
        un=u+nu*dt*((numpy.roll(u,-1,axis=0)-2*u+numpy.roll(u,1,axis=0))/dx**2
                   +(numpy.roll(u,-1,axis=1)-2*u+numpy.roll(u,1,axis=1))/dy**2)
        -dt/dx*(u-numpy.roll(u, 1, axis=0))*u-dt/dy*v*(u-numpy.roll(u, 1, axis=1))
        vn=v+nu*dt*((numpy.roll(v,-1,axis=0)-2*v+numpy.roll(v,1,axis=0))/dx**2
                   +(numpy.roll(v,-1,axis=1)-2*v+numpy.roll(v,1,axis=1))/dy**2)
        -dt/dy*(v-numpy.roll(v, 1, axis=1))*v-dt/dx*u*(v-numpy.roll(v, 1, axis=0))
        u = un.copy()
        v = vn.copy()
        u[0, :] = 1
        u[-1, :] = 1
        u[:, 0] = 1
        u[:, -1] = 1
    print("simtime:",time()-startTime)
    startTime=time()
    surface[0].remove()
    surface[0] = ax.plot_surface(X, Y, u, cmap=cm.viridis, rstride=2, cstride=2)
    surface[0] = ax.plot_surface(X, Y, v, cmap=cm.viridis, rstride=2, cstride=2)
    print("showtime:",time()-startTime)

ani = FuncAnimation(fig, update, frames=nt, interval=2000)

pyplot.show()
