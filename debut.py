import numpy as np
import math

def dist(a, b):
	return math.ceil(math.sqrt(math.pow(a[0]-b[0], 2) + math.pow(a[1]-b[1], 2)))


warehouses = [[0,0],[1,8],[5,5][5,6][9,0]]


drone = [6,6]


newPos = [0,0]
mini = 100000
for i in warehouses:
	res = dist(drone, i)
	if res < mini:
		mini = res
		newPos = i
drone = newPos
print drone

