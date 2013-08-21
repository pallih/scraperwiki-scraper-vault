import scraperwiki, gviz_api

#Keep the API key [private - via http://blog.scraperwiki.com/2011/10/19/tweeting-the-drilling/
import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    key=qsenv["KEY"]
    if 'progID' in qsenv: progID=qsenv['progID']
    else: progID='6'
    if 'full' in qsenv: full=qsenv['full']
    else: full=''
    if 'format' in qsenv: format=qsenv['format']
    else: format='json'
    if 'typ' in qsenv: typ=qsenv['typ']
    else: typ='prog'
    if 'awardID' in qsenv: awardID=qsenv['awardID']
    else: awardID=''
except:
    exit(-1)


import urllib2, json, networkx as nx
from networkx.readwrite import json_graph


def ascii(s): return "".join(i for i in s.encode('utf-8') if ord(i)<128)

def g(u):
    response= json.load(urllib2.urlopen(u+'?access_token='+str(key)))
    if 'results' in response: return response['results']
    else: return response['result']

'''
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

'''

def graphRoot(DG,title,root=1):
    DG.add_node(root,name=ascii(title))
    return DG,root

def gNodeAdd(DG,root,node,name):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name))
    DG.add_edge(root,node)
    return DG,node

def gNodeAdd2(DG,root,node,name,size=1):
    node=node+1
    #print str(root),'..',str(node)
    DG.add_node(node,name=ascii(name),size=int(size))
    DG.add_edge(root,node)
    return DG,node

DG=nx.DiGraph()
roots={}

#DG,roots['core']= gNodeAdd(DG,root,currid,'Core')
#currid=roots['core']

#DG,roots['option']= gNodeAdd(DG,root,currid,'Option')
#currid=roots['option']

if typ=='awardtree' and awardID!='':
    u='https://n2.online.lincoln.ac.uk/awards/id/'+str(awardID) #may need to check limits
    jdata=g(u)
    DG,roots['top']=graphRoot(DG,jdata['title'])
    currid=roots['top'] 
    curryears=[]
    tmpyearroots={}
    for prog in jdata['programmes']:
        year=prog['academic_year']['name']
        if year not in tmpyearroots:
            DG,currid=gNodeAdd(DG,roots['top'],currid,year)
            tmpyearroots[year]=currid
        DG,currid=gNodeAdd2(DG,tmpyearroots[year],currid,prog['programme_title'])
elif typ=='awardtree':
    u='https://n2.online.lincoln.ac.uk/awards/' #may need to check limits
    jdata=g(u)
    DG,roots['top']=graphRoot(DG,'University of Lincoln Awards')
    currid=roots['top'] 
    for award in jdata:
        DG,awardroot=gNodeAdd(DG,roots['top'],currid,award['title'])
        currid=awardroot
        u2=award['nucleus_url']
        ajdata=g(u2)
        curryears=[]
        tmpyearroots={}
        for prog in ajdata['programmes']:
            year=prog['academic_year']['name']
            if year not in tmpyearroots:
                DG,currid=gNodeAdd(DG,awardroot,currid,year)
                tmpyearroots[year]=currid
            DG,currid=gNodeAdd2(DG,tmpyearroots[year],currid,prog['programme_title'])

else: #typ=='prog' default
    u='https://n2.online.lincoln.ac.uk/programmes/id/'+str(progID)
    jdata=g(u)

    DG,roots['top']=graphRoot(DG,jdata['course_title'])
    currid=roots['top']

    levels={'core':{},'option':{}}

    for m in jdata['module_links']:
        mcode=m['module']['module_code']['code']
        mname=m['module']['title']
        mlevel=m['module']['level']['description']
        size=1
        if full!='':
            u2=m['module']['nucleus_url']
            j2=g(u2)
            size=int(j2['credit_rating'])
        if mlevel not in roots:
            DG,roots[mlevel]=gNodeAdd(DG,roots['top'],currid,mlevel)
            currid=roots[mlevel]
            DG,roots['core_'+mlevel]=gNodeAdd(DG,roots[mlevel],currid,"Core")
            currid=roots['core_'+mlevel]
            DG,roots['option_'+mlevel]=gNodeAdd(DG,roots[mlevel],currid,"Option")
            currid=roots['option_'+mlevel]
        if m['core']==True:
            DG,currid=gNodeAdd2(DG,roots['core_'+mlevel],currid,mcode,size)
        else:
            DG,currid=gNodeAdd2(DG,roots['option_'+mlevel],currid,mcode,size)
        tmproot=currid
        if full=='contact':
            for contact in j2['contact_times']:
                ct=contact['contact_type']['title']
                DG,currid=gNodeAdd2(DG,tmproot,currid,ct,contact['hours'])
        elif full=='assessment':
            DG,tmpfinal=gNodeAdd(DG,tmproot,currid,'Final Assessment')
            currid=tmpfinal
            DG,tmpcont=gNodeAdd(DG,tmproot,currid,'Continuous Assessment')
            currid=tmpcont
            for assessment in j2['assessments']:
                try: w=int(assessment['weighting'])#*int(j2['credit_rating'])
                except: w=0
                if assessment['final_assessment']==True:
                    DG,currid=gNodeAdd2(DG,tmpfinal,currid,assessment['assessment_method'],w)
                else:
                    DG,currid=gNodeAdd2(DG,tmpcont,currid,assessment['assessment_method'],w)

#--------
if format=='gexf':
    import networkx.readwrite.gexf as gf
    writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
    writer.add_graph(DG)
    scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")
    from xml.etree.cElementTree import tostring
    print tostring(writer.xml)
else: #format=='json'
    jdata = json_graph.tree_data(DG,root=1)#json_graph.node_link_data(DG)
    scraperwiki.utils.httpresponseheader("Content-Type", "text/json")
    print json_graph.dumps(jdata)