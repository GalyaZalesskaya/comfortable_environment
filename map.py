import requests, sys, os
from PIL import Image


def coordinates(x, y):
    lat = x
    lon = y
    zoom = 16
    type = "map"
    return (type, zoom, lat, lon)


def ll(lat, lon):
    return str(lon) + "," + str(lat)

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=ll(mp[2],mp[3]), z=mp[1], type=mp[0])
    response = requests.get(map_request)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
            file.write(response.content)
    return map_file

mp = coordinates(56.302358, 43.905130)
load_map(mp)

im = Image.open('map.jpg').convert('RGB')

water = 0
vegetation = 0

k = 0
for pixel in im.getdata():
    k += 1
    # print(pixel)
    if pixel == (184, 223, 245):
        water += 1
    elif pixel == (215, 242, 194) or pixel == (216, 242, 194) or pixel == (233, 248, 221):
        vegetation += 1

print('water=', water / k, ', vegetation=', vegetation / k)