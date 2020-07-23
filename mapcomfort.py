import numpy as np 
from imagesapi import imagesCoordinatesAPI
from imagesapi import imagesCoordinatesAPI_change
from imagesapi import imagesCoordinatesAPI_oneimage
from segmentation import imagesCoordinatesSegmentation
from map import marksMapsWaterVegatation
from imagesapi import adressToCoordinate
import os, glob, shutil, sys
from map_marks import Map
from PIL import Image
import math

Down_lock_in = 'pictures_in'
Down_lock_out = 'pictures_out'
Down_lock_tmp = 'pictures_tmp'
Down_lock_central = 'picture_central'
dlat = 0.009 #  шаг dlat 0.009 = 1 км на север
dlon = 0.016 #  шаг dlon 0.016 = 1 км на восток (получено имперически)

def inputUser():
	flag = True
	while (flag):
		print("Хотите вводить адрес места или координату? Введите + если адрес, - если координату")
		coordinate = input()
		if (coordinate == "+"):
			print("Введите город в котором вы хотите оценить комфортность?")
			City = str(input())
			print("Введите улицу")
			Street =str(input())
			print("Введите дом")
			Dom= str(input())
			print("Введите радиус")
			r= float(input())
			central_point = adressToCoordinate(City, Street, Dom)
			central_point_lat = float(central_point[1])
			central_point_lon = float(central_point[0])
			print(central_point_lat, central_point_lon)
			flag = False
		elif (coordinate == "-"):
			print("Введите широту")
			central_point_lat = float(input())
			print("Введите долготу")
			central_point_lon = float(input())
			print("Введите радиус")
			r= float(input())
			imagesCoordinatesAPI_oneimage(central_point_lat, central_point_lon, Down_lock_central)
			indexcentr=indexAnDropoutErrorImageFiles(Down_lock_central)
			if (len(indexcentr)>0):
				print("К сожалению, для заданной точки не найдено ни одной панорамы, попробуйте еще!!!")
				print("-------------------------------------------------------------------------------")
				flag = True
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте еще!!!")
			print("----------------------------------------------")
	weight = [0, 8, 0, 0, -10, 0, 0, 0, 10, 10, 0, 0, 0, 0, -10, 0, 0, 0, 0, 0, 0]
	flag = True
	while (flag):
		print("Положительно ли вы относитесь к зданиям? Поставьте + если да, - если нет")
		mark = input()
		if (mark == "+"):
			weight[2] = 10
			flag = False
		elif (mark == "-"):
			weight[2] = -10
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте  еще!!!!")
			print("----------------------------------------------")

	flag = True
	while (flag):
		print("Положительно ли вы относитесь к светофорам? Поставьте + если да, - если нет")
		mark = input()
		if (mark == "+"):
			weight[6] = 10
			flag = False
		elif (mark == "-"):
			weight[6] = -10
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте  еще!!!!")
			print("----------------------------------------------")

	flag = True
	while (flag):
		print("Положительно ли вы относитесь к дорожным знакам? Поставьте + если да, - если нет")
		mark = input()
		if (mark == "+"):
			weight[7] = 10
			flag = False
		elif (mark == "-"):
			weight[7] = -10
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте  еще!!!!")
			print("----------------------------------------------")

	flag = True
	while (flag):
		print("Положительно ли вы относитесь к людям? Поставьте + если да, - если нет")
		mark = input()
		if (mark == "+"):
			weight[11] = 10
			flag = False
		elif (mark == "-"):
			weight[11] = -10
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте  еще!!!!")
			print("----------------------------------------------")

	flag = True
	while (flag):
		print("Положительно ли вы относитесь к машинам на дороге? Поставьте + если да, - если нет")
		mark = input()
		if (mark == "+"):
			weight[13] = 10
			flag = False
		elif (mark == "-"):
			weight[13] = -10
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте  еще!!!!")
			print("----------------------------------------------")

	flag = True
	while (flag):
		print("Положительно ли вы относитесь к велосипедам на дороге? Поставьте + если да, - если нет")
		mark = input()
		if (mark == "+"):
			weight[18] = 10
			flag = False
		elif (mark == "-"):
			weight[18] = -10
			flag = False
		else:
			print("Вы ввели некорректные данные, попробуйте  еще!!!!")
			print("----------------------------------------------")
	return central_point_lat, central_point_lon, r,weight


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
                listindexerrorimages.append(count)
    return listindexerrorimages


def findCoordAroundPoint(Lat, Lon, radius, directory):
	#функция ищет координаты и их обзоры(360) в окрестности в квадрате радиуса r и записывает их в указанную директорию
	global indexeserror
	listcoord = []
	if (math.sqrt(radius ** 2 + radius ** 2) < 400):
		step = radius/2 # шаг в метрах
	if (math.sqrt(radius ** 2 + radius ** 2) < 800):
		step = radius/3 # шаг в метрах
	if (math.sqrt(radius ** 2 + radius ** 2) < 1400):
		step = radius/4 # шаг в метрах
	if (math.sqrt(radius ** 2 + radius ** 2) < 2000):
		step = radius/5 # шаг в метрах

	steplat = round(dlat*step/1000., 6)
	steplon = round(dlon *step/1000., 6)

	errorstep=200
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
		rightdown[0]-=steplat
		rightdown[1]+=steplon
		listcoord.append([round(rightdown[0], 6), round(rightdown[1], 6)])
		leftdown[0]-=steplat
		leftdown[1]-=steplon
		listcoord.append([round(leftdown[0], 6), round(leftdown[1], 6)])
		leftup[0]+=steplat
		leftup[1]-=steplon
		listcoord.append([round(leftup[0],6), round(leftup[1], 6)])
		upright[0]+=steplat
		upright[1]+=steplon
		listcoord.append([round(upright[0], 6), round(upright[1], 6)])
	listcoordcopy = listcoord[:]
	print("начальный список координат", listcoord)
	imagesCoordinatesAPI(listcoord , Down_lock_in)   #раскомментировать если хочешь делать запрос API
	indexeserror = list(set(indexAnDropoutErrorImageFiles(directory)))
	print("начальный список с ошибками" , indexeserror)
	for i in range(0,len(indexeserror)):
		lat=listcoord[indexeserror[i]][0]
		lon = listcoord[indexeserror[i]][1]
		imagesCoordinatesAPI_change(lat, lon, indexeserror[i], Down_lock_in)
	indexeserror = list(set(indexAnDropoutErrorImageFiles(Down_lock_in))) #записываем лист индексов с ошибками
	print("конечный список с ошибками" , indexeserror)
	return listcoordcopy , indexeserror

def markComfortArea(listcoord, indexeserror,central_point_lat, central_point_lon,r,weight):
	global sum_mark
	flaglist=[]
	print("All coordinates is ", len(listcoord))
	Marklist=imagesCoordinatesSegmentation(weight)
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
			if Marklist[i] < 2:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pm2rdm")
			elif Marklist[i] <= 6:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pm2ywm")
			else:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pm2gnm")
		else:
			if Marklist[i] < 2:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pmrds")
			elif Marklist[i] <= 6:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pmyws")
			else:
				flaglist.append(str(listcoord[i][1]) + "," + str(listcoord[i][0]) + "," + "pmgns")
	sum_mark=sum(Marklist)/len(Marklist)
	return flaglist,sum_mark

def moveFilesOtherFolder(lok_in, lok_out):
    folders = glob.glob(lok_in)
    os.mkdir(lok_out+"/"+str(central_point_lat)+","+str(central_point_lon))
    for file in folders:
        for f in glob.glob(file+'/*.png'):
            shutil.copy2(f,lok_out+"//"+str(central_point_lat)+","+str(central_point_lon)+"//")

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
	central_point_lat, central_point_lon, r ,weight= inputUser()
	Listcoord, Indexerror=findCoordAroundPoint(central_point_lat, central_point_lon, r, Down_lock_in)
	resultlist, com_l=markComfortArea(Listcoord, Indexerror,central_point_lat, central_point_lon,r,weight)
	Map(central_point_lat, central_point_lon, resultlist, r,com_l )
	moveFilesOtherFolder(Down_lock_in, Down_lock_tmp)
	removeFilesInFolder(Down_lock_tmp)
	savetxtCentralCoordAnRadius(central_point_lat, central_point_lon, r)

	print("Resalt raiting:\n")
	for i in range(len(resultlist)):
		print(resultlist[i], "\n")
	print('Comfort of area: ', sum_mark)

if __name__ == '__main__':
    sys.exit(main() or 0)

