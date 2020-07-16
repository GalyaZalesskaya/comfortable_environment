import requests, sys, os

def MapParams(lat,lon,zoom,mark,rad):
    lat = lat
    lon = lon
    zoom = zoom
    a_lat=lat-rad*0.000009
    a_lon=lon+rad*0.000016
    b_lat=lat+rad*0.000009
    b_lon=a_lon
    c_lat=a_lat
    c_lon=lon-rad*0.000016
    d_lat=b_lat
    d_lon=c_lon
    square="c:00FF00A0,f:00FF00A0,"+str(a_lon)+","+str(a_lat)+","+str(b_lon)+","+str(b_lat)+","+str(d_lon)+","+str(d_lat)+","+str(c_lon)+","+str(c_lat)+","+str(a_lon)+","+str(a_lat)
    for i in range(0,len(mark)-1):
        mark_v=mark[i]+"~"+mark[i+1]+"~"
    mark_v=mark_v[:-1]
    return (str(lon)+","+str(lat),zoom,mark_v,square)

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&pl={square}&z={z}&l={type}&pt={mark}".format(ll=mp[0], z=mp[1], type="map",mark=mp[2],square=mp[3])
    response = requests.get(map_request)
    #print(map_request)
    map_file = "map.jpg"
    with open(map_file, "wb") as file:
            file.write(response.content)
    return map_file

rad=200
mark=[str(43.905130)+","+str(56.302358)+","+"flag",str(43.905136)+","+str(56.302360)+","+"pmbls"]
mp = MapParams(56.30235,43.905130,16,mark,rad)
load_map(mp)