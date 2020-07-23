import urllib, os
import urllib.request
import requests
from yandex_geocoder import Client

key = "&key=" + "XXXXXXXXXX"
DownLoc = "pictures_in"


def GetStreetLL(Lat, Lon, Head, File, SaveLoc, R_search):
    base = r"https://maps.googleapis.com/maps/api/streetview"
    size = r"?size=1200x800&fov=120&radius="+str(R_search)+"&location="
    end = str(Lat) + "," + str(Lon) + "&heading=" + str(Head) + key
    MyUrl = base + size + end
    print(MyUrl)
    map_file = SaveLoc + "/" + File + ".png"
    response = requests.get(MyUrl)
    with open(map_file, "wb") as file:
        file.write(response.content)

def imagesCoordinatesAPI(DataList, SaveLoc, R_search):
    for i in range(len(DataList)):
        for a in range(0, 3):
            if a == 0:
                head = 0
            elif a == 1:
                head = 120
            else:
                head = 240
            lat = DataList[i][0]
            lon = DataList[i][1]
            if (i<10):
                fi = "Image_0" + str(i) + "_" + str(head)
                temp = GetStreetLL(lat, lon, head, fi, SaveLoc, R_search)
                fi = ""
            else:
                fi = "Image_" + str(i) + "_" + str(head)
                temp = GetStreetLL(lat, lon, head, fi, SaveLoc, R_search)
                fi = ""


def imagesCoordinatesAPI_oneimage(lat, lon, SaveLoc, R_search):
    head = 0
    fi = "Image_" + str(lat) + "," + str(lon)
    temp = GetStreetLL(lat, lon, head, fi, SaveLoc, R_search)
    fi = ""


def adressToCoordinate(city, street, dom):
    client = Client("1eaf6c9f-0eab-4fe5-b3cb-51c3b819f7b8")
    coordinates = client.coordinates(city + " " + street + " " + dom)
    return [coordinates[0], coordinates[1]]


 
