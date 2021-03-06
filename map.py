import requests, sys, os
from PIL import Image

def coordinates(x, y,rad):
    lat = x
    lon = y
    if rad <= 70:
        zoom = 18
    elif rad <= 140:
        zoom = 17
    elif rad <= 250:
        zoom = 16
    elif rad <= 500:
        zoom = 15
    elif rad <= 1100:
        zoom = 14
    else:
        zoom = 13
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

def marksMapsWaterVegatation(lat, lon,rad):
    mp = coordinates(lat, lon,rad)
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
    water_ratio = water / k
    vegetation_ratio = vegetation / k
    weight = [25, 20]
    sum_mark = weight[0]*water_ratio + weight[1]*vegetation_ratio
    return sum_mark
