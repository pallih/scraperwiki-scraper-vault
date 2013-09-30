import scraperwiki, gviz_api

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    key=qsenv["KEY"]
    if 'progID' in qsenv: progID=qsenv['progID']
    else: progID='6'
except:
    exit(-1)

page_template = """
<html>
  <head>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['treemap']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);
     var treemap = new google.visualization.TreeMap(document.getElementById('visualization'));
     treemap.draw(json_data, {maxDepth:2,maxPostDepth:1});

     var json_data2 = new google.visualization.DataTable(%(json2)s, 0.6);
     var treemap2 = new google.visualization.TreeMap(document.getElementById('visualization2'));
     treemap2.draw(json_data2, {maxDepth:2,maxPostDepth:1});
    }
  </script>
  </head>
  <body>
    <h1>Programme breakdown (core modules)</h1>
    <p>Experimential views over course data eg assessment breakdown and contact types over *all* *core* modules</p>
    <p>Pass in via the URL:</p>
    <ul>
        <li><tt>progID=</tt> the programme ID</li>
    </ul>
    <p>Experimental: the credit rating/number of CATS points associated with a module is used as a way of further weighting the assessment weighting of a module: block size is credit_rating * assessment weighting</p>
    <p>Note that higher level courses tend to count more towards to the final award; this level based weighting is not reflected.</p>
    <hr/>
    <p><strong>Assessement view:</strong> view the breakdown of assessment percentages by module. Colour denotes level (experimental, may be broken).</p>
    <div id="visualization" style="width: 900px; height: 700px;" ></div>
    <hr/>
    <p><strong>Contact view:</strong> view the breakdown of contact hours.</p>
    <div id="visualization2" style="width: 900px; height: 700px;" ></div>
    <hr/>
    <p>So what other treemaps naturally come to mind? At a module level, it would be easy enough to do similar maps:</p>
    <ul>
        <li><strong>Assessment:</strong> split into final/not final and then by assessment type and weighting</li>
        <li><strong>Contact:</strong> split into contact type and hours</li>
    </ul>
    <p>At the programme level, there are also other tweaks we could make. For example, it might make sense to have "level" as the first child of the programme, and then carve out views on that basis?</p>
  </body>
</html>
"""


import urllib2,json
def g(u): return json.load(urllib2.urlopen(u+'?access_token='+str(key)))['result']

u='https://n2.online.lincoln.ac.uk/programmes/id/'+str(progID)
jdata=g(u)

def itemise(item,parent,weighting,level=''):
    try:
        if weighting!='': weighting=int(weighting) #weighting=math.log10(int(weighting))
        else: weighting=0
    except:
        weighting=0
    try: level=int(level.replace('Level ',''))
    except: level=0
    item={'item':item,'parent':parent,'weighting':weighting,'level':level}
    return item

def itemise2(item,parent,hours,level=''):
    try:
        if hours!='': hours=int(hours)
        else: hours=0
    except:
        hours=0
    try: level=int(level.replace('Level ',''))
    except: level=0
    item={'item':item,'parent':parent,'hours':hours,'level':level}
    return item

#--- Assessment
ddata=[]
typs={}

ddata.append(itemise("Assessment Weighting",'',0))
ddata.append(itemise("Final Assessment","Assessment Weighting",0))
ddata.append(itemise("Not Final Assessment","Assessment Weighting",0))
typs['Final Assessment']=[]
typs['Not Final Assessment']=[]

#-----Contact
ddata2=[]
typs2=[]

ddata2.append(itemise2("Contact Time",'',0))

for m in jdata['module_links']:
    if m['core']==True:
        u2=m['module']['nucleus_url']
        j2=g(u2)

        for assessment in j2['assessments']:
            if assessment['final_assessment']==True:
                atyp="Final Assessment"
                hack='.'
            else:
                atyp="Not Final Assessment"
                hack=''
            if assessment['assessment_method'] not in typs[atyp]:
                typs[atyp].append(assessment['assessment_method'])
                ddata.append(itemise(assessment['assessment_method']+hack,atyp,0))
            ddata.append(itemise(j2['module_code']['code']+' ('+str(assessment['id'])+')',assessment['assessment_method']+hack,int(j2['credit_rating'])*assessment['weighting'],j2['level']['description']))

        for contact in j2['contact_times']:
            ct=contact['contact_type']['title']
            if ct not in typs2:
                typs2.append(ct)
                ddata2.append(itemise2(ct,"Contact Time",0))
            ddata2.append(itemise2(j2['module_code']['code']+' ('+contact['contact_type']['contact_type_category']['title']+' '+str(contact['id'])+')', ct, contact['hours'], j2['level']['description']))


description={"item":('string','item'),"parent":('string','parent'),"weighting":('number','weighting'),"level":('number','level')}
ddata_table = gviz_api.DataTable(description)
ddata_table.LoadData(ddata)
json = ddata_table.ToJSon(columns_order=("item", "parent","weighting",'level'))

description2={"item":('string','item'),"parent":('string','parent'),"hours":('number','hours'),"level":('number','level')}
ddata_table2 = gviz_api.DataTable(description2)
ddata_table2.LoadData(ddata2)
json2 = ddata_table2.ToJSon(columns_order=("item", "parent","hours",'level'))

#--------
print page_template % vars()import scraperwiki, gviz_api

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    key=qsenv["KEY"]
    if 'progID' in qsenv: progID=qsenv['progID']
    else: progID='6'
except:
    exit(-1)

page_template = """
<html>
  <head>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['treemap']});
    google.setOnLoadCallback(drawTable);
    function drawTable() {
     var json_data = new google.visualization.DataTable(%(json)s, 0.6);
     var treemap = new google.visualization.TreeMap(document.getElementById('visualization'));
     treemap.draw(json_data, {maxDepth:2,maxPostDepth:1});

     var json_data2 = new google.visualization.DataTable(%(json2)s, 0.6);
     var treemap2 = new google.visualization.TreeMap(document.getElementById('visualization2'));
     treemap2.draw(json_data2, {maxDepth:2,maxPostDepth:1});
    }
  </script>
  </head>
  <body>
    <h1>Programme breakdown (core modules)</h1>
    <p>Experimential views over course data eg assessment breakdown and contact types over *all* *core* modules</p>
    <p>Pass in via the URL:</p>
    <ul>
        <li><tt>progID=</tt> the programme ID</li>
    </ul>
    <p>Experimental: the credit rating/number of CATS points associated with a module is used as a way of further weighting the assessment weighting of a module: block size is credit_rating * assessment weighting</p>
    <p>Note that higher level courses tend to count more towards to the final award; this level based weighting is not reflected.</p>
    <hr/>
    <p><strong>Assessement view:</strong> view the breakdown of assessment percentages by module. Colour denotes level (experimental, may be broken).</p>
    <div id="visualization" style="width: 900px; height: 700px;" ></div>
    <hr/>
    <p><strong>Contact view:</strong> view the breakdown of contact hours.</p>
    <div id="visualization2" style="width: 900px; height: 700px;" ></div>
    <hr/>
    <p>So what other treemaps naturally come to mind? At a module level, it would be easy enough to do similar maps:</p>
    <ul>
        <li><strong>Assessment:</strong> split into final/not final and then by assessment type and weighting</li>
        <li><strong>Contact:</strong> split into contact type and hours</li>
    </ul>
    <p>At the programme level, there are also other tweaks we could make. For example, it might make sense to have "level" as the first child of the programme, and then carve out views on that basis?</p>
  </body>
</html>
"""


import urllib2,json
def g(u): return json.load(urllib2.urlopen(u+'?access_token='+str(key)))['result']

u='https://n2.online.lincoln.ac.uk/programmes/id/'+str(progID)
jdata=g(u)

def itemise(item,parent,weighting,level=''):
    try:
        if weighting!='': weighting=int(weighting) #weighting=math.log10(int(weighting))
        else: weighting=0
    except:
        weighting=0
    try: level=int(level.replace('Level ',''))
    except: level=0
    item={'item':item,'parent':parent,'weighting':weighting,'level':level}
    return item

def itemise2(item,parent,hours,level=''):
    try:
        if hours!='': hours=int(hours)
        else: hours=0
    except:
        hours=0
    try: level=int(level.replace('Level ',''))
    except: level=0
    item={'item':item,'parent':parent,'hours':hours,'level':level}
    return item

#--- Assessment
ddata=[]
typs={}

ddata.append(itemise("Assessment Weighting",'',0))
ddata.append(itemise("Final Assessment","Assessment Weighting",0))
ddata.append(itemise("Not Final Assessment","Assessment Weighting",0))
typs['Final Assessment']=[]
typs['Not Final Assessment']=[]

#-----Contact
ddata2=[]
typs2=[]

ddata2.append(itemise2("Contact Time",'',0))

for m in jdata['module_links']:
    if m['core']==True:
        u2=m['module']['nucleus_url']
        j2=g(u2)

        for assessment in j2['assessments']:
            if assessment['final_assessment']==True:
                atyp="Final Assessment"
                hack='.'
            else:
                atyp="Not Final Assessment"
                hack=''
            if assessment['assessment_method'] not in typs[atyp]:
                typs[atyp].append(assessment['assessment_method'])
                ddata.append(itemise(assessment['assessment_method']+hack,atyp,0))
            ddata.append(itemise(j2['module_code']['code']+' ('+str(assessment['id'])+')',assessment['assessment_method']+hack,int(j2['credit_rating'])*assessment['weighting'],j2['level']['description']))

        for contact in j2['contact_times']:
            ct=contact['contact_type']['title']
            if ct not in typs2:
                typs2.append(ct)
                ddata2.append(itemise2(ct,"Contact Time",0))
            ddata2.append(itemise2(j2['module_code']['code']+' ('+contact['contact_type']['contact_type_category']['title']+' '+str(contact['id'])+')', ct, contact['hours'], j2['level']['description']))


description={"item":('string','item'),"parent":('string','parent'),"weighting":('number','weighting'),"level":('number','level')}
ddata_table = gviz_api.DataTable(description)
ddata_table.LoadData(ddata)
json = ddata_table.ToJSon(columns_order=("item", "parent","weighting",'level'))

description2={"item":('string','item'),"parent":('string','parent'),"hours":('number','hours'),"level":('number','level')}
ddata_table2 = gviz_api.DataTable(description2)
ddata_table2.LoadData(ddata2)
json2 = ddata_table2.ToJSon(columns_order=("item", "parent","hours",'level'))

#--------
print page_template % vars()