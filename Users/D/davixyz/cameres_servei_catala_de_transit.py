import scraperwiki, urllib, simplejson

def search_geo(_idcam):
    for x2 in result2["features"]:
        if str(x2["properties"]["id_camera"])==str(_idcam):
            return x2["geometry"]["coordinates"]
    return ""


url1 = "http://mct.gencat.cat/sct-gis/wfs?service=WFS&version=1.0.0&request=GetFeature&maxFeatures=300&outputFormat=json&srsName=EPSG:4326&typeName=cite:mct2_cameres"

url2 = "http://mct.gencat.cat/sct-gis/wfs?service=WFS&version=1.0.0&request=GetFeature&maxFeatures=300&outputFormat=json&srsName=EPSG:4326&typeName=cite:mct2_cam_punt_active"

url_img_cam = "http://www.gencat.cat/cgi-bin/cit/veure_camera2?cam="

result1 = simplejson.load(urllib.urlopen(url1))
result2 = simplejson.load(urllib.urlopen(url2))

strresult = ""

strresult = '<?xml version="1.0" encoding="UTF-8"?>'
strresult += '<kml><Document>'

for x in result1["features"]:


    idcam = x["id"][x["id"].find(".")+1:]
    _camera = search_geo(idcam)
    _src_img = ""
    if not x["properties"]["nom_fitxer"] is None and x["properties"]["url"].find("../")>-1:
        _src_img = url_img_cam + x["properties"]["nom_fitxer"] + ".jpg"
    elif not x["properties"]["url"] is None:
        _src_img = x["properties"]["url"]

    if _camera!="" and not _src_img=="": 
        strresult +='<Placemark><name>' + x["properties"]["nom_municipi"] + ". " + x["properties"]["codi_carretera"] + '</name><Point><coordinates>' + str(_camera[0]) + "," + str(_camera[1]) + '</coordinates></Point>'
        strresult +='<description><img src="' + _src_img  + '" /></description></Placemark>'

        scraperwiki.datastore.save(unique_keys=["id"],data={"id":idcam, "name":x["properties"]["nom_municipi"] + ". " + x["properties"]["codi_carretera"],"img":_src_img, "lat":str(_camera[1]),"lng":str(_camera[0])}) 

strresult += '</Document></kml>'

scraperwiki.datastore.save(unique_keys=["id"],data={"id":9999, "name":strresult,"img":"", "lat":"","lng":""}) 

#print strresult 


