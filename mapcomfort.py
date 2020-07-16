import numpy as np 
from imagesapi import imagesCoordinatesAPI
from segmentation import imagesCoordinatesSegmentation
#import math as m

central_point_lat = 56.281279 
central_point_lon = 43.989542 
r=200
dlat = 0.009 #  шаг dlat 0.009 = 1 км на север
dlon = 0.016 #  шаг dlon 0.016 = 1 км на восток (получено имперически)

def findCoordAroundPoint(Lat, Lon, radius):
	#функция ищет равномерно координаты в окрестности в квадрате радиуса r
	global N
	listcoord = []
	step = 100. # шаг в метрах
	steplat = dlat*step/1000. 
	steplon = dlon *step/1000.
	N = int(radius/step)
	right = [Lat, Lon]
	rightdown = [Lat, Lon]
	down = [Lat, Lon]
	leftdown = [Lat, Lon]
	left = [Lat, Lon]
	leftup = [Lat, Lon]
	up = [Lat, Lon]
	upright = [Lat, Lon]
	listcoord.append([Lat, Lon])
	for i in range(N):
		#right[0]+=0
		right[1]+=steplon
		listcoord.append([right[0], right[1]])
		rightdown[0]-=steplat
		rightdown[1]+=steplon
		listcoord.append([rightdown[0], rightdown[1]])
		down[0]-=steplat
		#down[1]+=0
		listcoord.append([down[0], down[1]])
		leftdown[0]-=steplat
		leftdown[1]-=steplon
		listcoord.append([leftdown[0], leftdown[1]])
		#left[0]-=0
		left[1]-=steplon
		listcoord.append([left[0], left[1]])
		leftup[0]+=steplat
		leftup[1]-=steplon
		listcoord.append([leftup[0], leftup[1]])
		up[0]+=steplat
		#up[1]-=0
		listcoord.append([up[0], up[1]])
		upright[0]+=steplat
		upright[1]+=steplon
		listcoord.append([upright[0], upright[1]])
	return listcoord

def markComfortArea(listcoord):
	imagesCoordinatesAPI(listcoord)
	marklist=[]
	print("All coordinates is ", len(listcoord))
	for i in range(len(listcoord)):
		marklist.append(imagesCoordinatesSegmentation(i))
	return sum(marklist)/N

Listcoord=findCoordAroundPoint(central_point_lat, central_point_lon, r)
print('Comfort of area: ', markComfortArea(Listcoord))



#print(len(findCoordAroundPoint(central_point_lat, central_point_lon, 100.)))
#print(findCoordAroundPoint(central_point_lat, central_point_lon, 100.))