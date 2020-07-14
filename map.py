import requests, sys, os


class MapParams(object):
    def __init__(self):
        self.lat = 56.326210
        self.lon = 44.079732
        self.zoom = 16
        self.type = "map"

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
            file.write(response.content)
    return map_file

mp = MapParams()
load_map(mp)

from PIL import Image

im = Image.open('map.jpg')

water = 0
vegetation = 0

k = 0
for pixel in im.getdata():
    k += 1
    # print(pixel)
    if pixel == (227) or pixel == (229):
        water += 1
    elif pixel == (214):
        vegetation += 1

print('water=', water, ', vegetation=', vegetation, k)