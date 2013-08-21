import scraperwiki
import gviz_api
import time
from time import mktime
from datetime import datetime
import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'sha' in get: sha=get['sha']
    else: sha='Q30'
else:
    sha='Q30'

sourcescraper = 'nhs_sit_reps'

page_template = """
<html>
  <head>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['annotatedtimeline']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);

     var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization'));
      annotatedtimeline.draw(json_data, {'displayAnnotations': false});

    }
  </script>
  </head>
  <body>
    <h1>NHS Sitrep Demo - "D&amp;V, Norovirus" for SHA %(sha)s</h1>
    
    <hr/>
    <div id="visualization" style="width: 900px; height: 700px;" ></div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( sourcescraper )
# where value!="-"
q = 'SHA,facetB,fromDateStr, sum(value) as value from `id_7` where SHA=="'+sha+'" group by SHA,facetB,fromDateStr'
data = scraperwiki.sqlite.select(q)

ddata=[]
dtmp={}
for item in data:
    item['fromDate']= datetime.fromtimestamp(mktime(time.strptime(item['fromDateStr'], "%Y-%m-%d")))
    #item['toDate']=datetime.fromtimestamp(mktime(time.strptime(item['toDateStr'], "%Y-%m-%d")))
    k=item['fromDateStr']+item['SHA']
    if k not in dtmp:
        dtmp[k]={}
    for k2 in ['SHA','fromDate']: dtmp[k][k2]=item[k2]
    if item['facetB']=='Beds closed norovirus':
        dtmp[k]['closed']=item['value']
        dtmp[k]['t1']=item['facetB']
    else: #Beds closed unocc
        dtmp[k]['unocc']=item['value']
        dtmp[k]['t2']=item['facetB']

for item in dtmp:    
    ddata.append(dtmp[item])

#description={"SHA":('string','SHA'),"name":('string','name'),"value":('number','value'),"toDate":('date','toDate'),"fromDate":('date','fromDate'),"toDateStr":('string','toDateStr'),"fromDateStr":('string','fromDateStr')}

#description={"SHA":('string','SHA'),"value":('number','value'),"fromDate":('date','fromDate'),"fromDateStr":('string','fromDateStr')}
description={"SHA":('string','SHA'),"closed":('number','closed'),"t1":('string','t1'),"t2":('string','t2'),"unocc":('number','unocc'),"fromDate":('date','fromDate') }
data_table = gviz_api.DataTable(description)
data_table.LoadData(ddata)

json=data_table.ToJSon(columns_order=("fromDate","closed", "t1","unocc","t2"))

print page_template % vars()
