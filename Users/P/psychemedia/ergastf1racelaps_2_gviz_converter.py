import gviz_api, urllib, simplejson
import scraperwiki


import cgi, os
qstring=os.getenv("QUERY_STRING")

debug=False
if debug:
    year='2012'
    race='1'
    callback=''
else:
    try:
        get = dict(cgi.parse_qsl(qstring))
        year=get['year']
        race=get['race']
        if 'callback' in get: callback=get['callback']
        else: callback=''
    except: exit(-1)



#url='http://ergast.com/api/f1/2011/5/laps.json?limit=2000'
url='http://ergast.com/api/f1/'+str(year)+'/'+str(race)+'/laps.json?limit=2000'

#Example of:
## how to use the Google gviz Python library to convert lap data from ergast F1 api to gviz

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html

'''{"MRData":{"xmlns":"http:\/\/ergast.com\/mrd\/1.2","series":"f1","url":"http://ergast.com/api/f1/2011/5/laps.json","limit":"150","offset":"0","total":"1491","RaceTable":{"season":"2011","round":"5","Races":[{"season":"2011","round":"5","url":"http:\/\/en.wikipedia.org\/wiki\/2011_Spanish_Grand_Prix","raceName":"Spanish GP","Circuit":{"circuitId":"catalunya","url":"http://en.wikipedia.org/wiki/Circuit_de_Catalunya","circuitName":"Circuit de Catalunya","Location":{"lat":"41.57","long":"2.26111","locality":"Montmeló","country":"Spain"}},"date":"2011-05-22","time":"12:00:00Z","Laps":[{"number":"1","Timings":[{"driverId":"alonso","position":"1","time":"1:34.494"},{"driverId":"vettel","position":"2","time":"1:35.274"},{"driverId":"webber","position":"3","time":"1:36.329"},{"driverId":"hamilton","position":"4","time":"1:36.991"},'''

description = {"lap":("number","Lap"), "driverId": ("string", "Driver ID"),"position": ("number", "Position"),"time": ("string", "Time"),"stime":("number","Time (s)")}

data=[]

jdata=simplejson.load(urllib.urlopen(url))
for lap in jdata['MRData']['RaceTable']['Races'][0]['Laps']:
    #print lap
    lapnum=int(lap['number'])
    tmp=lap['Timings']
    for t in tmp:
        predata={}
        predata['lap']=lapnum
        for k in t:
            predata[k]=t[k]
        predata['position']=int(predata['position'])
        predata['stime']= 60*int(predata['time'].split(':')[0])+  float(predata['time'].split(':')[1])
        data.append(predata)

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("lap", "position","driverId","time","stime" ),order_by="lap,position")

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
if callback!='':
    print callback+'('+json+')'
else: print jsonimport gviz_api, urllib, simplejson
import scraperwiki


import cgi, os
qstring=os.getenv("QUERY_STRING")

debug=False
if debug:
    year='2012'
    race='1'
    callback=''
else:
    try:
        get = dict(cgi.parse_qsl(qstring))
        year=get['year']
        race=get['race']
        if 'callback' in get: callback=get['callback']
        else: callback=''
    except: exit(-1)



#url='http://ergast.com/api/f1/2011/5/laps.json?limit=2000'
url='http://ergast.com/api/f1/'+str(year)+'/'+str(race)+'/laps.json?limit=2000'

#Example of:
## how to use the Google gviz Python library to convert lap data from ergast F1 api to gviz

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html

'''{"MRData":{"xmlns":"http:\/\/ergast.com\/mrd\/1.2","series":"f1","url":"http://ergast.com/api/f1/2011/5/laps.json","limit":"150","offset":"0","total":"1491","RaceTable":{"season":"2011","round":"5","Races":[{"season":"2011","round":"5","url":"http:\/\/en.wikipedia.org\/wiki\/2011_Spanish_Grand_Prix","raceName":"Spanish GP","Circuit":{"circuitId":"catalunya","url":"http://en.wikipedia.org/wiki/Circuit_de_Catalunya","circuitName":"Circuit de Catalunya","Location":{"lat":"41.57","long":"2.26111","locality":"Montmeló","country":"Spain"}},"date":"2011-05-22","time":"12:00:00Z","Laps":[{"number":"1","Timings":[{"driverId":"alonso","position":"1","time":"1:34.494"},{"driverId":"vettel","position":"2","time":"1:35.274"},{"driverId":"webber","position":"3","time":"1:36.329"},{"driverId":"hamilton","position":"4","time":"1:36.991"},'''

description = {"lap":("number","Lap"), "driverId": ("string", "Driver ID"),"position": ("number", "Position"),"time": ("string", "Time"),"stime":("number","Time (s)")}

data=[]

jdata=simplejson.load(urllib.urlopen(url))
for lap in jdata['MRData']['RaceTable']['Races'][0]['Laps']:
    #print lap
    lapnum=int(lap['number'])
    tmp=lap['Timings']
    for t in tmp:
        predata={}
        predata['lap']=lapnum
        for k in t:
            predata[k]=t[k]
        predata['position']=int(predata['position'])
        predata['stime']= 60*int(predata['time'].split(':')[0])+  float(predata['time'].split(':')[1])
        data.append(predata)

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("lap", "position","driverId","time","stime" ),order_by="lap,position")

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
if callback!='':
    print callback+'('+json+')'
else: print json