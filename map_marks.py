import requests, sys, os

def Map(lat,lon,mark,rad,com_l):
    lat = lat
    lon = lon
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
    a_lat=lat-rad*0.000009
    a_lon=lon+rad*0.000016
    b_lat=lat+rad*0.000009
    b_lon=a_lon
    c_lat=a_lat
    c_lon=lon-rad*0.000016
    d_lat=b_lat
    d_lon=c_lon
    color_dict = {0: 'FFC9C9A0', 1: 'F9FFB5A0', 2: 'D0FFB8A0'}
    if com_l < 0:
        color = "c:" + color_dict[0] + ",f:" + color_dict[0] + ","
    elif com_l <= 2:
        color = "c:" + color_dict[1] + ",f:" + color_dict[1] + ","
    else:
        color = "c:" + color_dict[2] + ",f:" + color_dict[2] + ","
    square = color + str(a_lon) + "," + str(a_lat) + "," + str(b_lon) + "," + str(b_lat) + "," + str(d_lon) + "," + str(
        d_lat) + "," + str(c_lon) + "," + str(c_lat) + "," + str(a_lon) + "," + str(a_lat)
    print("len mark:", len(mark))
    mark_v=""
    for i in range(0, len(mark) - 1):
        mark_v = mark_v+mark[i] + "~" + mark[i + 1] + "~"
    mark_v = mark_v[:-1]
    print("mark", mark_v)
    load_map(str(lon) + "," + str(lat),zoom,mark_v,square)

def load_map(ll,zoom,mark,square):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&pl={square}&z={z}&l={type}&pt={mark}".format(ll=ll, z=zoom, type="map",mark=mark,square=square)
    response = requests.get(map_request)
    print(map_request)
    map_file = "map_com_level.jpg"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file
