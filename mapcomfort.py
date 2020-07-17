import numpy as np 
from imagesapi import imagesCoordinatesAPI
from segmentation import imagesCoordinatesSegmentation
from map import marksMapsWaterVegatation
#import math as m

central_point_lat = 56.281279 
central_point_lon = 43.989542 
r=200
dlat = 0.009 #  шаг dlat 0.009 = 1 км на север
dlon = 0.016 #  шаг dlon 0.016 = 1 км на восток (получено имперически)

def findCoordAroundPoint(Lat, Lon, radius):
	#функция ищет равномерно координаты в окрестности в квадрате радиуса r
	listcoord = []
	step = 150. # шаг в метрах
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
	#imagesCoordinatesAPI(listcoord)
	global sum_mark
	flaglist=[]
	print("All coordinates is ", len(listcoord))
	Marklist=imagesCoordinatesSegmentation()
	addition_mark = marksMapsWaterVegatation(central_point_lat, central_point_lon)
	print("оценки", Marklist)
	print("доп. оценка", addition_mark)
	for i in range(len(Marklist)):
		Marklist[i]=0.5*(Marklist[i] + addition_mark)
		print
		if (i == 0):	
			if Marklist[i]<0:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2rds")
			elif Marklist[i]<=2:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2yws")
			elif Marklist[i]<=5:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2ors")
			else:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2gns")
		else:
			if Marklist[i]<0:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pmrds")
			elif Marklist[i]<=2:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2yws")
			elif Marklist[i]<=5:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2ors")
			else:
				flaglist.append(str(listcoord[i][0])+","+str(listcoord[i][1])+","+"pm2gns")
	sum_mark=sum(Marklist)/len(Marklist)
	return flaglist

Listcoord=findCoordAroundPoint(central_point_lat, central_point_lon, r)

#marksMapsWaterVegatation(lat, lon):
resultlist=markComfortArea(Listcoord)
print("Resalt raiting:\n")
for i in range(len(resultlist)):
	print(resultlist[i], "\n")
print('Comfort of area: ', sum_mark)