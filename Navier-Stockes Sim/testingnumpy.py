import numpy

array=numpy.ones((3,3))
array[0][0]=42
array[1][0]=41
array[2][0]=40
print(array)
print(numpy.roll(array,axis=0,shift=1)[0][0])
print(array)
