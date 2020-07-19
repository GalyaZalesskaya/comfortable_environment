import numpy as np 
from imagesapi import imagesCoordinatesAPI
from segmentation import imagesCoordinatesSegmentation
from map import marksMapsWaterVegatation
from imagesapi import adressToCoordinate
import os, glob, shutil, sys
from map_marks import Map
from PIL import Image
#import math as m

r=400.
dlat = 0.009 #  шаг dlat 0.009 = 1 км на север
dlon = 0.016 #  шаг dlon 0.016 = 1 км на восток (получено имперически)
City= "Нижний Новогород"
Street = "Донецкая"
Dom = "7"
Down_lock_in = 'pictures_in'
Down_lock_out = 'pictures_out'
Down_lock_tmp = 'pictures_tmp'

central_point = adressToCoordinate(City, Street, Dom)
central_point_lat = float(central_point[1])
central_point_lon = float(central_point[0])
print(central_point_lat, central_point_lon)

def indexAnDropoutErrorImageFiles(directory):
    folders = glob.glob(directory)
    listindexerrorimages = []
    count=-1
    indexerrorfile=0
    for file in folders:
        for f in glob.glob(file+'/*.png'):
            count+=1                            # считается сколько всего файлов(фото) в папке
            im = Image.open(f).convert('RGB')
            numberallpixels=0
            errorpixels=0
            for pixel in im.getdata():
                numberallpixels+=1
                if pixel == (228, 227, 223):
                    errorpixels+=1                        # считается сколько ненужных пикселей содержит фото
                if (errorpixels > 50000):  								# ошибочное фото содерижт 405335 px из 409600 px
                    listindexerrorimages.append(count // 3)
                    f = f.replace('\\','/')
                    path = os.path.join(os.path.abspath(os.path.dirname('__file__')), f)
                    os.remove(path)
                    break
    print("listindexerrorimages ", listindexerrorimages)
    return listindexerrorimages


def findCoordAroundPoint(Lat, Lon, radius, directory):
	#функция ищет координаты и их обзоры(360) в окрестности в квадрате радиуса r и записывает их в указанную директорию
	global indexeserror
	listcoord = []
	step = radius/2 # шаг в метрах
	steplat = round(dlat*step/1000., 6)
	steplon = round(dlon *step/1000., 6)

	errorstep=100
	errorsteplat = round(dlat*errorstep/1000., 6)
	errorsteplon = round(dlon *errorstep/1000., 6)
	N = int(radius/step) - 1
	if (N==0):
		N=1
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
		#right[1]+=steplon
		#listcoord.append([right[0], right[1]])
		rightdown[0]-=steplat
		rightdown[1]+=steplon
		listcoord.append([round(rightdown[0], 6), round(rightdown[1], 6)])
		#down[0]-=steplat
		#down[1]+=0
		#listcoord.append([down[0], down[1]])
		leftdown[0]-=steplat
		leftdown[1]-=steplon
		listcoord.append([round(leftdown[0], 6), round(leftdown[1], 6)])
		#left[0]-=0
		#left[1]-=steplon
		#listcoord.append([left[0], left[1]])
		leftup[0]+=steplat
		leftup[1]-=steplon
		listcoord.append([round(leftup[0],6), round(leftup[1], 6)])
		#up[0]+=steplat
		#up[1]-=0
		#listcoord.append([up[0], up[1]])
		upright[0]+=steplat
		upright[1]+=steplon
		listcoord.append([round(upright[0], 6), round(upright[1], 6)])
		print(listcoord)
	imagesCoordinatesAPI(listcoord , Down_lock_in)   #раскомментировать если хочешь делать запрос API
	indexeserror = list(set(indexAnDropoutErrorImageFiles(directory)))
	print("indexeserror", indexeserror)
	return [listcoord , indexeserror]

def markComfortArea(listcoord, indexeserror):
	global sum_mark
	flaglist=[]
	print("All coordinates is ", len(listcoord))
	Marklist=imagesCoordinatesSegmentation()
	addition_mark = marksMapsWaterVegatation(central_point_lat, central_point_lon,r)
	print("listerror ", indexeserror)
	if (len(indexeserror)>0):
		for i in range(len(indexeserror)):		#вставляем оценку центральной вместо багпикч
			Marklist.insert(indexeserror[i], Marklist[0])
	print("оценки", Marklist)
	print("доп. оценка", addition_mark)
	for i in range(len(Marklist)):
		Marklist[i] = Marklist[i] + addition_mark
		print
		if (i == 0):
			if Marklist[i] < 0.5:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pm2rdm")
			elif Marklist[i] <= 3:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pm2ywm")
			else:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pm2gnm")
		else:
			if Marklist[i] < 0.5:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pmrds")
			elif Marklist[i] <= 3:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pmyws")
			else:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pmgns")
	sum_mark=sum(Marklist)/len(Marklist)
	return flaglist,sum_mark

def moveFilesOtherFolder(lok_in, lok_out, radius):
    folders = glob.glob(lok_in)
    os.mkdir(lok_out+"/"+str(central_point_lat)+","+str(central_point_lon)+","+str(radius))
    for file in folders:
        for f in glob.glob(file+'/*.png'):
            shutil.copy2(f,lok_out+"//"+ str(central_point_lat) + "," + str(central_point_lon)+"//")

def removeFilesInFolder(lok):
    folders = glob.glob(lok)
    for file in folders:
        for f in glob.glob(file+'/*.png'):
            os.remove(f)

def savetxtCentralCoordAnRadius(Lat, Lon, radius):
      f = open('savecoord.txt', 'a')
      f.write(str(Lat)+ '\n')
      f.write(str(Lon)+ '\n')
      f.write(str(radius)+ '\n')

def main():
	Listcoord=findCoordAroundPoint(central_point_lat, central_point_lon, r, Down_lock_in)
	resultlist, com_l=markComfortArea(Listcoord[0], Listcoord[1])
	Map(central_point_lat, central_point_lon, resultlist, r,com_l )
	moveFilesOtherFolder(Down_lock_in, Down_lock_tmp, r)
	removeFilesInFolder(Down_lock_tmp)
	savetxtCentralCoordAnRadius(central_point_lat, central_point_lon, r)

	print("Resalt raiting:\n")
	for i in range(len(resultlist)):
		print(resultlist[i], "\n")
	print('Comfort of area: ', sum_mark)

if __name__ == '__main__':
    sys.exit(main() or 0)

