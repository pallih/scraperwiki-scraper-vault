# Examples of how to use treemaps to display points to date and by round for a mutli round sports event.
# In this case, we use F1 data to show treemaps detailing points awarded in the Driver and Constructor Chanmpionships

import urllib,simplejson,gviz_api

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'year' in get:
        year=get['year']
else:
    year='2012'


url='http://ergast.com/api/f1/'+str(year)+'/results.json?limit=1000'

ejson=simplejson.load(urllib.urlopen(url))
rdata=ejson['MRData']['RaceTable']['Races']

#print rdata

page_template = """
<html>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['treemap']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);
 var treemap = new google.visualization.TreeMap(document.getElementById('visualization'));
 treemap.draw(json_data, {});
 
var json_data2 = new google.visualization.DataTable(%(json2)s, 0.6);
 var treemap2 = new google.visualization.TreeMap(document.getElementById('visualization2'));
 treemap2.draw(json_data2, {maxDepth:2});

var json_data3 = new google.visualization.DataTable(%(json3)s, 0.6);
 var treemap3 = new google.visualization.TreeMap(document.getElementById('visualization3'));
 treemap3.draw(json_data3, {});
 
    }
  </script>
  <body><h1>F1 results test (<a href="http://ergast.com/">Ergast API</a>)</h1>
<div>Exploring the idea of using Google Viz Tree Map widgets to display F1 2012 Drivers' and Constructors' Championship Standings. Note that colours are currently random; I think a reasonable colour scheme might be to use red/green for down/up change between last but one race and most recent race? The actual points totals aren't shown either, which they really need to be, at each level.</div>
<div>To explore different years, put eg <em>?year=2011</em> on to the end of the page URL.(Hmmm.. could do one for dirvers/teams over multiple years???? See also eg http://intelligentf1.wordpress.com/2012/04/04/different-look-historic-f1-data/ in this context )</div>
<div>Click on a square to 'look inside' it/tunnel down on the data. Right click goes back up a level (I think? Erm....?!)</div>
<div>To explore: can I tweak the labels? Can I display auto-calculated points values in the label at each level?</div>
<div id="visualization"></div>
<div id="visualization2"></div>
<div id="visualization3"></div>
  </body>
</html>
"""



description={"item":('string','item'),"parent":('string','parent'),"points":('number','points')}

def itemise(item,parent,points):
    item={'item':item,'parent':parent,'points':int(points)}
    return item


ddata=[]
cdata=[]
c2data=[]
constructors=[]

season=rdata[0]['season']
drivers=[]
rns={}
ddata.append(itemise(season,'',0))
cdata.append(itemise(season,'',0))
c2data.append(itemise(season,'',0))
for round in rdata:
    race=round['raceName']
    for driver in round['Results']:
        dname=" ".join([ driver['Driver']['givenName'], driver['Driver']['familyName'] ])
        constructor=driver['Constructor']['name']
        if constructor not in constructors:
            rns[constructor]=[]
            constructors.append(constructor)
            cdata.append(itemise(constructor,season,0))
            c2data.append(itemise(constructor,season,0))
        points=int(driver['points'])
        rn=race+' ['+constructor+']'
        if rn not in rns[constructor]:
            rns[constructor].append(rn)
            c2data.append(itemise(rn,constructor,0))
        if dname not in drivers:
            drivers.append(dname)
            ddata.append(itemise(dname,season,0))
            #make a bad assumption for now - that driver will stick with a team throughout the season
            cdata.append(itemise(dname,constructor,0))
        c2data.append(itemise(dname+' ['+str(points)+' points, ('+race+')',rn,points))
        ddata.append(itemise(race+' ['+str(points)+' points, ('+driver['number']+')]',dname,points))
        cdata.append(itemise(race+' ['+str(points)+' points, ('+driver['Driver']['driverId']+')]',dname,points))
        

ddata_table = gviz_api.DataTable(description)
ddata_table.LoadData(ddata)
json = ddata_table.ToJSon(columns_order=("item", "parent","points"))

cdata_table = gviz_api.DataTable(description)
cdata_table.LoadData(cdata)
json2 = cdata_table.ToJSon(columns_order=("item", "parent","points"))

c2data_table = gviz_api.DataTable(description)
c2data_table.LoadData(c2data)
json3 = c2data_table.ToJSon(columns_order=("item", "parent","points"))
#print json2

#print json
print page_template % vars()
