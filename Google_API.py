import urllib, os
import urllib.request
import requests

key = "&key=" + "xxxxxxxx"
DownLoc = "xxxxxxxxx"

def GetStreetLL(Lat,Lon,Head,File,SaveLoc):
    base = r"https://maps.googleapis.com/maps/api/streetview"
    size = r"?size=1200x800&fov=60&location="
    end = str(Lat) + "," + str(Lon) + "&heading=" + str(Head) + key
    MyUrl = base + size + end
    print(MyUrl)
    map_file = File + ".png"
    response = requests.get(MyUrl)
    with open(map_file, "wb") as file:
            file.write(response.content)

DataList = [(56.331765, 44.008905),
            (56.2646423, 44.012892),
            (56.263737, 44.0145472),
            (56.2786812, 43.9793558),
            (56.2605652, 43.9672871),
            (56.1553526, 44.0605514),
            (56.2983557, 43.9970424),
            (56.3124118, 44.0368413),
            (56.3061993, 44.0377582),
            (56.3579899, 43.8263388),
            (56.2668518, 43.8590221),
            (56.3244536, 44.0093166),
            (56.3890136, 43.7381222),
            (56.3854128, 43.7378569)]

ct = 0
for i in DataList:
    ct += 1
    for a in range(0,3):
        if a==0:
            head=0
        elif a==1:
            head=120
        else:
            head=240
        lat=i[0]
        lon=i[1]
        fi = "Image_" + str(ct)+"_"+str(head)
        temp = GetStreetLL(lat,lon,head,fi,DownLoc)
        fi=""