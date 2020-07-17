import requests, sys, os
from PIL import Image

def MapParams(lat, lon,z):
    lat = lat
    lon = lon
    zoom = z
    type = "map"
    return (str(lon) + "," + str(lat),zoom,type)

def comf_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp[0], z=mp[1], type=mp[2])
    response = requests.get(map_request)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
            file.write(response.content)
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

    #print('water=', water, ', vegetation=', vegetation, k)
    return water/k,vegetation/k

comf_map(mp=MapParams(56.326210,44.079732,16))
