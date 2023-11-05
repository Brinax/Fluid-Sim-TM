import numpy
import time
u = numpy.array((0, 1, 2, 3, 4, 5))

for i in range(1, len(u)):
    print(u[i] - u[i-1])

u[1:] - u[0:-1]

nx = 81
ny = 81
nt = 100
c = 1
dx = 2 / (nx - 1)
dy = 2 / (ny - 1)
sigma = .2
dt = sigma * dx

x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((ny, nx)) ##create a 1xn vector of 1's
un = numpy.ones((ny, nx)) 

###Assign initial conditions

u[int(.5 / dy): int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

print(time.time())
initialTime=time.time()
u = numpy.ones((ny, nx))
u[int(.5 / dy): int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

for n in range(nt + 1): ##loop across number of time steps
    un = u.copy()
    u[1:, 1:] = (un[1:, 1:] - (c * dt / dx * (un[1:, 1:] - un[1:, 0:-1])) -
                              (c * dt / dy * (un[1:, 1:] - un[0:-1, 1:])))
    u[0, :] = 1
    u[-1, :] = 1
    u[:, 0] = 1
    u[:, -1] = 1
print(time.time()-initialTime)