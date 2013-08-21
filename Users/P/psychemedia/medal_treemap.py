import scraperwiki, gviz_api
sourcescraper = 'nbc_olympic_medalscrape'

import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'typ' in get: typ=get['typ']
    else: typ='medalCountryEvent'
else:
    typ='medalCountryEvent'

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
    }
  </script>
  </head>
  <body>
    <h1>Medal Treemap Demo</h1>
    <p>An alternative series of views over the medal tables... They are posted as illustrative examples only, sketches in an exploration of how this sort of visual representation may be used to display medal standings. Each table helps illustrate a separate sort of story - I'll try to post a quick summary of what each view might be good for when I get a chance. Some of the views will also benefit greatly from different colourings. However, the Google Visualisation treemap widgets used in this demo arenlt very good at colouring; I think the d3.js treemap is a bit more flexible...</p>
    <p>Note that the tables may get a little out of date - they used scraped data and the scraper only runs once a day...</p>
    <p>Usage: click to zoom in, right click to zoom out.</p>
    <p>For alternative views, set the ?typ= URL parameter to one of <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=medalCountryEvent"><em>medalCountryEvent</em></a>, <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=countryEventMedal"><em>countryEventMedal</em></a>, <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=countryMedalEvent"><em>countryMedalEvent</em></a>, <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=eventCountryMedal"><em>eventCountryMedal</em></a>, <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=medalEventCountry"><em>medalEventCountry</em></a>, <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=eventMedalCountry"><em>eventMedalCountry</em></a>. For example, <a href="https://views.scraperwiki.com/run/medal_treemap/?typ=countryMedalEvent"><tt>https://views.scraperwiki.com/run/medal_treemap/?typ=countryMedalEvent</tt></a></p>
    <hr/>
    <div id="visualization" style="width: 900px; height: 700px;" ></div>
  </body>
</html>
"""

scraperwiki.sqlite.attach( sourcescraper )

q = '* FROM "medalStandings"'
data = scraperwiki.sqlite.select(q)

#print data


def itemise(item,parent,medalcount=0):
    item={'item':item,'parent':parent,'medalcount':medalcount}
    return item

medals=["Gold","Silver","Bronze"]

#The form of this function is slightly different to the others
#I left it in to show the evolution of the function
def medalCountryEvent(data):
    ddata=[]
    alist=[]
    root="Medal Table"
    ddata.append(itemise(root,'',0))
    for m in medals:
        ddata.append(itemise(m,root,0))
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                acm=ac+m
                node=ac+" ("+m+")"
                if acm not in alist:
                    alist.append(acm)
                    ddata.append(itemise(node,m))
                ddata.append(itemise(bc+ " ("+ac+" "+m+" ["+str(row[m])+"])",node,row[m]))
    return ddata
   
description={"item":('string','item'),"parent":('string','parent'),"medalcount":('number','medalcount')}

#ddata_table = gviz_api.DataTable(description)
#ddata_table.LoadData(ddata)
#json=ddata_table.ToJSon(columns_order=("item", "parent","medalcount"))

#The following functions can be generalised and replaced by a single parameterised function
#I'm just a little, erm, too tired to do it right now...
def countryEventMedal(data):
    ddata=[]
    alist=[]
    rlist=[]
    root="Country Event Medal Table"
    ddata.append(itemise(root,''))
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                bcc=bc+ac
                node=bc+" ("+ac+")"
                if ac not in rlist:
                    rlist.append(ac)
                    ddata.append(itemise(ac,root))
                if bcc not in alist:
                    alist.append(bcc)
                    ddata.append(itemise(node,ac))
                ddata.append(itemise(m+ " ("+bc+" "+ac+" ["+str(row[m])+"])",node,row[m]))
    return ddata

#ddata_table = gviz_api.DataTable(description)
#ddata_table.LoadData(ddata)
#json2=ddata_table.ToJSon(columns_order=("item", "parent","medalcount"))

def countryMedalEvent(data):
    ddata=[]
    alist=[]
    rlist=[]
    root="Country Medal Event Table"
    ddata.append(itemise(root,''))
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                mac=m+ac
                node=m+" ("+ac+")"
                if ac not in rlist:
                    rlist.append(ac)
                    ddata.append(itemise(ac,root))
                if mac not in alist:
                    alist.append(mac)
                    ddata.append(itemise(node,ac))
                ddata.append(itemise(bc+ " ("+m+" "+ac+" ["+str(row[m])+"])",node,row[m]))
    return ddata

def eventCountryMedal(data):
    ddata=[]
    alist=[]
    rlist=[]
    root="Event Country Medal Table"
    ddata.append(itemise(root,''))
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                abc=ac+bc
                node=ac+" ("+bc+")"
                if bc not in rlist:
                    rlist.append(bc)
                    ddata.append(itemise(bc,root))
                if abc not in alist:
                    alist.append(abc)
                    ddata.append(itemise(node,bc))
                ddata.append(itemise(m+ " ("+ac+" "+bc+" ["+str(row[m])+"])",node,row[m]))
    return ddata

def medalEventCountry(data):
    ddata=[]
    alist=[]
    rlist=[]
    root="Medal Event Country Table"
    ddata.append(itemise(root,''))
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                bcm=bc+m
                node=bc+" ("+m+")"
                if m not in rlist:
                    rlist.append(m)
                    ddata.append(itemise(m,root))
                if bcm not in alist:
                    alist.append(bcm)
                    ddata.append(itemise(node,m))
                ddata.append(itemise(ac+ " ("+bc+" "+m+" ["+str(row[m])+"])",node,row[m]))
    return ddata

def eventMedalCountry(data):
    ddata=[]
    alist=[]
    rlist=[]
    root="Event Medal Country Table"
    ddata.append(itemise(root,''))
    for row in data:
        ac=row['cc']
        bc=row['Event']
        for m in medals:
            if row[m]>0:
                mbc=m+bc
                node=m+" ("+bc+")"
                if bc not in rlist:
                    rlist.append(bc)
                    ddata.append(itemise(bc,root))
                if mbc not in alist:
                    alist.append(mbc)
                    ddata.append(itemise(node,bc))
                ddata.append(itemise(ac+ " ("+m+" "+bc+" ["+str(row[m])+"])",node,row[m]))
    return ddata

if typ=='medalCountryEvent': ddata=medalCountryEvent(data)
elif typ=='countryMedalEvent': ddata=countryMedalEvent(data)
elif typ=='countryEventMedal': ddata=countryEventMedal(data)
elif typ=='eventCountryMedal': ddata=eventCountryMedal(data)
elif typ=='medalEventCountry': ddata=medalEventCountry(data)
elif typ=='eventMedalCountry': ddata=eventMedalCountry(data)
else: ddata=medalCountryEvent(data)

ddata_table = gviz_api.DataTable(description)
ddata_table.LoadData(ddata)
json=ddata_table.ToJSon(columns_order=("item", "parent","medalcount"))

#NEED TO TAKE A DEEP BREATH AND ABSTRACT A SINGLE PARAMETERISED FUNCTION TO HANDLE ALL PERMUTATIONS...
print page_template % vars()