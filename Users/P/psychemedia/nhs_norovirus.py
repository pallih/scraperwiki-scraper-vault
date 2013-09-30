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
sourcescraper2='nhs_sit_reps_2011'

page_template = """
<html>
  <head>
  <title>Norovirus sitrep</title>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['annotatedtimeline']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);
     var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization'));
      annotatedtimeline.draw(json_data, {'displayAnnotations': false, 'max':%(max)s});

     var json_data2 = new google.visualization.DataTable(%(json2)s, 0.6);
     var annotatedtimeline2 = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization2'));
      annotatedtimeline2.draw(json_data2, {'displayAnnotations': false,'max':%(max)s});

     var json_data = new google.visualization.DataTable(%(json3)s, 0.6);
     var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization3'));
      annotatedtimeline.draw(json_data, {'displayAnnotations': false, 'max':%(maxTrust)s});

     var json_data2 = new google.visualization.DataTable(%(json4)s, 0.6);
     var annotatedtimeline2 = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization4'));
      annotatedtimeline2.draw(json_data2, {'displayAnnotations': false,'max':%(maxTrust)s});

    }
  </script>
  </head>
  <body>
    <h1>NHS Sitrep Demo - "D&amp;V, Norovirus"</h1>
    <p>Data scraped from the NHS Winter sitrep spreadsheets <a href="http://www.dh.gov.uk/en/Publicationsandstatistics/Statistics/Performancedataandstatistics/DailySituationReports/index.htm">2011/12</a> and <a href="http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports/">2012/13</a></p>
<p>Data values correspond to: <em>Beds closed norovirus</em> and <em>Beds closed unocc</em> reports.</p>
<p>Read more on OpenLearn: <a href="http://www.open.edu/openlearn/science-maths-technology/mathematics-and-statistics/statistics/diary-data-sleuth-data-scraping-the-sick-bucket">Diary of a data sleuth: Data-scraping the sick bucket</a></p>
<p>For a more general take, see <a href="http://glimmer.rstudio.com/psychemedia/nhssitrep/">NHS Situation Reports Viewer</a></p>
    <hr/>
<p>This first pair of charts totals up the bed counts:</p>
<div>
    <div id="visualization" style="display: inline-block; width: 690px; height: 700px;" ></div>
    <div id="visualization2" style="display: inline-block;width: 690px; height: 700px;" ></div>
</div>
<hr/>
<p>This second pair of charts counts up the number of Trusts reporting affected bed count values &gt; 0:</p>
<div>
    <div id="visualization3" style="display: inline-block; width: 690px; height: 700px;" ></div>
    <div id="visualization4" style="display: inline-block;width: 690px; height: 700px;" ></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( sourcescraper )
scraperwiki.sqlite.attach( sourcescraper2 )


#---beds closed
# where value!="-"
q = 'facetB,fromDateStr,count(Name) as count, sum(value) as value from nhs_sit_reps.id_7 where value > 0 group by facetB,fromDateStr'
data = scraperwiki.sqlite.select(q)

max=0
maxTrust=0

ddata2=[]
dtmp={}
for item in data:
    item['fromDate']= datetime.fromtimestamp(mktime(time.strptime(item['fromDateStr'], "%Y-%m-%d")))
    #item['toDate']=datetime.fromtimestamp(mktime(time.strptime(item['toDateStr'], "%Y-%m-%d")))
    k=item['fromDateStr']
    if k not in dtmp:
        dtmp[k]={}
    dtmp[k]['fromDate12']=item['fromDate']
    if item['facetB']=='Beds closed norovirus':
        dtmp[k]['closed12']=item['value']
        dtmp[k]['t1_12']=item['facetB']
        dtmp[k]['closed12Trust']=item['count']
    else: #Beds closed unocc
        dtmp[k]['unocc12']=item['value']
        dtmp[k]['t2_12']=item['facetB']
        dtmp[k]['unocc12Trust']=item['count']

for item in dtmp:    
    ddata2.append(dtmp[item])
    if int(dtmp[item]['closed12'])>max: max=int(dtmp[item]['closed12'])
    if int(dtmp[item]['unocc12'])>max: max=int(dtmp[item]['unocc12'])
    if int(dtmp[item]['closed12Trust'])>maxTrust: maxTrust=int(dtmp[item]['closed12Trust'])
    if int(dtmp[item]['unocc12Trust'])>maxTrust: maxTrust=int(dtmp[item]['unocc12Trust'])

q = 'facetB,fromDateStr,count(Name) as count, sum(value) as value from nhs_sit_reps_2011.id_8 where value > 0 group by facetB,fromDateStr'
data = scraperwiki.sqlite.select(q)

ddata=[]
dtmp={}
for item in data:
    item['fromDate']= datetime.fromtimestamp(mktime(time.strptime(item['fromDateStr'], "%Y-%m-%d")))
    #item['toDate']=datetime.fromtimestamp(mktime(time.strptime(item['toDateStr'], "%Y-%m-%d")))
    k=item['fromDateStr']
    if k not in dtmp:
        dtmp[k]={}
    dtmp[k]['fromDate11']=item['fromDate']
    if item['facetB']=='Beds closed norovirus':
        dtmp[k]['closed11']=item['value']
        dtmp[k]['t1_11']=item['facetB']
        dtmp[k]['closed11Trust']=item['count']
    else: #Beds closed unocc
        dtmp[k]['unocc11']=item['value']
        dtmp[k]['t2_11']=item['facetB']
        dtmp[k]['unocc11Trust']=item['count']

for item in dtmp:    
    ddata.append(dtmp[item])
    if int(dtmp[item]['closed11'])>max: max=int(dtmp[item]['closed11'])
    if int(dtmp[item]['unocc11'])>max: max=int(dtmp[item]['unocc11'])
    if int(dtmp[item]['closed11Trust'])>maxTrust: maxTrust=int(dtmp[item]['closed11Trust'])
    if int(dtmp[item]['unocc11Trust'])>maxTrust: maxTrust=int(dtmp[item]['unocc11Trust'])
#description={"SHA":('string','SHA'),"name":('string','name'),"value":('number','value'),"toDate":('date','toDate'),"fromDate":('date','fromDate'),"toDateStr":('string','toDateStr'),"fromDateStr":('string','fromDateStr')}

#description={"SHA":('string','SHA'),"value":('number','value'),"fromDate":('date','fromDate'),"fromDateStr":('string','fromDateStr')}
description={"closed11":('number','closed11'),"t1_11":('string','t1_11'),"t2_11":('string','t2_11'),"unocc11":('number','unocc11'),"fromDate11":('date','fromDate11')}
data_table = gviz_api.DataTable(description)
data_table.LoadData(ddata)

json=data_table.ToJSon(columns_order=("fromDate11","closed11", "t1_11","unocc11","t2_11"))

description2={"closed12":('number','closed12'),"t1_12":('string','t1_12'),"t2_12":('string','t2_12'),"unocc12":('number','unocc12'),"fromDate12":('date','fromDate12')}
data_table2 = gviz_api.DataTable(description2)
data_table2.LoadData(ddata2)

json2=data_table2.ToJSon(columns_order=("fromDate12","closed12", "t1_12","unocc12","t2_12"))

#---
#description={"SHA":('string','SHA'),"name":('string','name'),"value":('number','value'),"toDate":('date','toDate'),"fromDate":('date','fromDate'),"toDateStr":('string','toDateStr'),"fromDateStr":('string','fromDateStr')}

#description={"SHA":('string','SHA'),"value":('number','value'),"fromDate":('date','fromDate'),"fromDateStr":('string','fromDateStr')}
description={"closed11Trust":('number','closed11Trust'),"t1_11":('string','t1_11'),"t2_11":('string','t2_11'),"unocc11Trust":('number','unocc11Trust'),"fromDate11":('date','fromDate11')}
data_table = gviz_api.DataTable(description)
data_table.LoadData(ddata)

json3=data_table.ToJSon(columns_order=("fromDate11","closed11Trust", "t1_11","unocc11Trust","t2_11"))

description2={"closed12Trust":('number','closed12Trust'),"t1_12":('string','t1_12'),"t2_12":('string','t2_12'),"unocc12Trust":('number','unocc12Trust'),"fromDate12":('date','fromDate12')}
data_table2 = gviz_api.DataTable(description2)
data_table2.LoadData(ddata2)

json4=data_table2.ToJSon(columns_order=("fromDate12","closed12Trust", "t1_12","unocc12Trust","t2_12"))
#---

print page_template % vars()
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
sourcescraper2='nhs_sit_reps_2011'

page_template = """
<html>
  <head>
  <title>Norovirus sitrep</title>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['annotatedtimeline']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);
     var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization'));
      annotatedtimeline.draw(json_data, {'displayAnnotations': false, 'max':%(max)s});

     var json_data2 = new google.visualization.DataTable(%(json2)s, 0.6);
     var annotatedtimeline2 = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization2'));
      annotatedtimeline2.draw(json_data2, {'displayAnnotations': false,'max':%(max)s});

     var json_data = new google.visualization.DataTable(%(json3)s, 0.6);
     var annotatedtimeline = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization3'));
      annotatedtimeline.draw(json_data, {'displayAnnotations': false, 'max':%(maxTrust)s});

     var json_data2 = new google.visualization.DataTable(%(json4)s, 0.6);
     var annotatedtimeline2 = new google.visualization.AnnotatedTimeLine(
      document.getElementById('visualization4'));
      annotatedtimeline2.draw(json_data2, {'displayAnnotations': false,'max':%(maxTrust)s});

    }
  </script>
  </head>
  <body>
    <h1>NHS Sitrep Demo - "D&amp;V, Norovirus"</h1>
    <p>Data scraped from the NHS Winter sitrep spreadsheets <a href="http://www.dh.gov.uk/en/Publicationsandstatistics/Statistics/Performancedataandstatistics/DailySituationReports/index.htm">2011/12</a> and <a href="http://transparency.dh.gov.uk/2012/10/26/winter-pressures-daily-situation-reports/">2012/13</a></p>
<p>Data values correspond to: <em>Beds closed norovirus</em> and <em>Beds closed unocc</em> reports.</p>
<p>Read more on OpenLearn: <a href="http://www.open.edu/openlearn/science-maths-technology/mathematics-and-statistics/statistics/diary-data-sleuth-data-scraping-the-sick-bucket">Diary of a data sleuth: Data-scraping the sick bucket</a></p>
<p>For a more general take, see <a href="http://glimmer.rstudio.com/psychemedia/nhssitrep/">NHS Situation Reports Viewer</a></p>
    <hr/>
<p>This first pair of charts totals up the bed counts:</p>
<div>
    <div id="visualization" style="display: inline-block; width: 690px; height: 700px;" ></div>
    <div id="visualization2" style="display: inline-block;width: 690px; height: 700px;" ></div>
</div>
<hr/>
<p>This second pair of charts counts up the number of Trusts reporting affected bed count values &gt; 0:</p>
<div>
    <div id="visualization3" style="display: inline-block; width: 690px; height: 700px;" ></div>
    <div id="visualization4" style="display: inline-block;width: 690px; height: 700px;" ></div>
</div>
  </body>
</html>
"""


scraperwiki.sqlite.attach( sourcescraper )
scraperwiki.sqlite.attach( sourcescraper2 )


#---beds closed
# where value!="-"
q = 'facetB,fromDateStr,count(Name) as count, sum(value) as value from nhs_sit_reps.id_7 where value > 0 group by facetB,fromDateStr'
data = scraperwiki.sqlite.select(q)

max=0
maxTrust=0

ddata2=[]
dtmp={}
for item in data:
    item['fromDate']= datetime.fromtimestamp(mktime(time.strptime(item['fromDateStr'], "%Y-%m-%d")))
    #item['toDate']=datetime.fromtimestamp(mktime(time.strptime(item['toDateStr'], "%Y-%m-%d")))
    k=item['fromDateStr']
    if k not in dtmp:
        dtmp[k]={}
    dtmp[k]['fromDate12']=item['fromDate']
    if item['facetB']=='Beds closed norovirus':
        dtmp[k]['closed12']=item['value']
        dtmp[k]['t1_12']=item['facetB']
        dtmp[k]['closed12Trust']=item['count']
    else: #Beds closed unocc
        dtmp[k]['unocc12']=item['value']
        dtmp[k]['t2_12']=item['facetB']
        dtmp[k]['unocc12Trust']=item['count']

for item in dtmp:    
    ddata2.append(dtmp[item])
    if int(dtmp[item]['closed12'])>max: max=int(dtmp[item]['closed12'])
    if int(dtmp[item]['unocc12'])>max: max=int(dtmp[item]['unocc12'])
    if int(dtmp[item]['closed12Trust'])>maxTrust: maxTrust=int(dtmp[item]['closed12Trust'])
    if int(dtmp[item]['unocc12Trust'])>maxTrust: maxTrust=int(dtmp[item]['unocc12Trust'])

q = 'facetB,fromDateStr,count(Name) as count, sum(value) as value from nhs_sit_reps_2011.id_8 where value > 0 group by facetB,fromDateStr'
data = scraperwiki.sqlite.select(q)

ddata=[]
dtmp={}
for item in data:
    item['fromDate']= datetime.fromtimestamp(mktime(time.strptime(item['fromDateStr'], "%Y-%m-%d")))
    #item['toDate']=datetime.fromtimestamp(mktime(time.strptime(item['toDateStr'], "%Y-%m-%d")))
    k=item['fromDateStr']
    if k not in dtmp:
        dtmp[k]={}
    dtmp[k]['fromDate11']=item['fromDate']
    if item['facetB']=='Beds closed norovirus':
        dtmp[k]['closed11']=item['value']
        dtmp[k]['t1_11']=item['facetB']
        dtmp[k]['closed11Trust']=item['count']
    else: #Beds closed unocc
        dtmp[k]['unocc11']=item['value']
        dtmp[k]['t2_11']=item['facetB']
        dtmp[k]['unocc11Trust']=item['count']

for item in dtmp:    
    ddata.append(dtmp[item])
    if int(dtmp[item]['closed11'])>max: max=int(dtmp[item]['closed11'])
    if int(dtmp[item]['unocc11'])>max: max=int(dtmp[item]['unocc11'])
    if int(dtmp[item]['closed11Trust'])>maxTrust: maxTrust=int(dtmp[item]['closed11Trust'])
    if int(dtmp[item]['unocc11Trust'])>maxTrust: maxTrust=int(dtmp[item]['unocc11Trust'])
#description={"SHA":('string','SHA'),"name":('string','name'),"value":('number','value'),"toDate":('date','toDate'),"fromDate":('date','fromDate'),"toDateStr":('string','toDateStr'),"fromDateStr":('string','fromDateStr')}

#description={"SHA":('string','SHA'),"value":('number','value'),"fromDate":('date','fromDate'),"fromDateStr":('string','fromDateStr')}
description={"closed11":('number','closed11'),"t1_11":('string','t1_11'),"t2_11":('string','t2_11'),"unocc11":('number','unocc11'),"fromDate11":('date','fromDate11')}
data_table = gviz_api.DataTable(description)
data_table.LoadData(ddata)

json=data_table.ToJSon(columns_order=("fromDate11","closed11", "t1_11","unocc11","t2_11"))

description2={"closed12":('number','closed12'),"t1_12":('string','t1_12'),"t2_12":('string','t2_12'),"unocc12":('number','unocc12'),"fromDate12":('date','fromDate12')}
data_table2 = gviz_api.DataTable(description2)
data_table2.LoadData(ddata2)

json2=data_table2.ToJSon(columns_order=("fromDate12","closed12", "t1_12","unocc12","t2_12"))

#---
#description={"SHA":('string','SHA'),"name":('string','name'),"value":('number','value'),"toDate":('date','toDate'),"fromDate":('date','fromDate'),"toDateStr":('string','toDateStr'),"fromDateStr":('string','fromDateStr')}

#description={"SHA":('string','SHA'),"value":('number','value'),"fromDate":('date','fromDate'),"fromDateStr":('string','fromDateStr')}
description={"closed11Trust":('number','closed11Trust'),"t1_11":('string','t1_11'),"t2_11":('string','t2_11'),"unocc11Trust":('number','unocc11Trust'),"fromDate11":('date','fromDate11')}
data_table = gviz_api.DataTable(description)
data_table.LoadData(ddata)

json3=data_table.ToJSon(columns_order=("fromDate11","closed11Trust", "t1_11","unocc11Trust","t2_11"))

description2={"closed12Trust":('number','closed12Trust'),"t1_12":('string','t1_12'),"t2_12":('string','t2_12'),"unocc12Trust":('number','unocc12Trust'),"fromDate12":('date','fromDate12')}
data_table2 = gviz_api.DataTable(description2)
data_table2.LoadData(ddata2)

json4=data_table2.ToJSon(columns_order=("fromDate12","closed12Trust", "t1_12","unocc12Trust","t2_12"))
#---

print page_template % vars()
