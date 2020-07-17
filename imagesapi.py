import urllib, os
import urllib.request
import requests

key = "&key=" + "AIzaSyCHxteYGq8iTPyZGf_KO0yAF4Wo_EfHHaU"
DownLoc = "pictures_in/"

def GetStreetLL(Lat,Lon,Head,File,SaveLoc):
    base = r"https://maps.googleapis.com/maps/api/streetview"
    size = r"?size=1200x800&fov=120&location="
    end = str(Lat) + "," + str(Lon) + "&heading=" + str(Head) + key
    MyUrl = base + size + end
    print(MyUrl)
    map_file = SaveLoc + File + ".png"
    response = requests.get(MyUrl)
    with open(map_file, "wb") as file:
            file.write(response.content)

def imagesCoordinatesAPI(DataList):
    for i in range(len(DataList)):
        for a in range(0,3):
            if a==0:
                head=0
            elif a==1:
                head=120
            else:
                head=240
            lat=DataList[i][0]
            lon=DataList[i][1]
            fi = "Image_" + str(i)+"_"+str(head)
            temp = GetStreetLL(lat,lon,head,fi,DownLoc)
            fi=""
