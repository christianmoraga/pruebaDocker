import numpy
from sklearn.metrics import r2_score

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22,23,24,25]
y = [100,100,80,60,60,55,60,65,70,10,10,76,78,79,90,99,100,100,114,113,112]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

speed = mymodel(25)
print(speed)